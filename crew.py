
import os

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool

from agents.crisis_analyst import create_crisis_analyst
from agents.supplier_agent import create_supplier_agent
from agents.inventory_agent import create_inventory_agent
from agents.logistics_agent import create_logistics_agent
from agents.risk_agent import create_risk_agent
from agents.recovery_manager import create_recovery_manager

from tools.supplier_tools import find_alternative_suppliers
from tools.inventory_tools import check_inventory
from tools.logistics_tools import compare_transport_options

load_dotenv()


# GROQ CONFIGURATION

def get_llm():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b"
    )

    return LLM(
        model=f"groq/{model}",
        api_key=api_key,
        temperature=0.2
    )


# OUTPUT LIMITER

def compact_output(result, limit=2200):

    result = str(result)

    if len(result) > limit:
        return result[:limit] + "\n[Output shortened.]"

    return result


# SUPPLIER TOOL

@tool("Supplier Search Tool")
def supplier_search_tool(product: str, required_quantity: int) -> str:
    """Find alternative suppliers and check their available stock."""

    result = find_alternative_suppliers(
        product,
        required_quantity
    )

    return compact_output(result)


# INVENTORY TOOL

@tool("Inventory Analysis Tool")
def inventory_analysis_tool(product: str, required_quantity: int) -> str:
    """Check warehouse inventory and calculate shortages."""

    result = check_inventory(
        product,
        required_quantity
    )

    return compact_output(result)


# LOGISTICS TOOL

@tool("Logistics Comparison Tool")
def logistics_comparison_tool(deadline_days: int) -> str:
    """Compare transport options against the delivery deadline."""

    result = compare_transport_options(deadline_days)

    return compact_output(result)


# MAIN WORKFLOW

def run_supply_chain_analysis(
    product,
    quantity,
    supplier,
    delay_days,
    deadline_days,
    problem
):

    llm = get_llm()

    # CREATE SIX AGENTS

    crisis_agent = create_crisis_analyst(llm)

    supplier_agent = create_supplier_agent(
        llm,
        supplier_search_tool
    )

    inventory_agent = create_inventory_agent(
        llm,
        inventory_analysis_tool
    )

    logistics_agent = create_logistics_agent(
        llm,
        logistics_comparison_tool
    )

    risk_agent = create_risk_agent(llm)

    recovery_agent = create_recovery_manager(llm)

    # TASK 1: CRISIS ANALYSIS

    crisis_task = Task(
        description=f"""
        Analyze this supply chain disruption.

        Product: {product}
        Quantity: {quantity}
        Supplier: {supplier}
        Delay: {delay_days} days
        Deadline: {deadline_days} days
        Problem: {problem}

        Identify the cause, severity, and immediate impact.
        Clearly mention missing information.
        Do not invent facts.

        Maximum 100 words.
        """,
        expected_output="A concise crisis summary with severity.",
        agent=crisis_agent
    )

    # TASK 2: SUPPLIER ANALYSIS

    supplier_task = Task(
        description=f"""
        Find alternative suppliers for {product}.

        Required quantity: {quantity}
        Current supplier: {supplier}

        Use the Supplier Search Tool.

        Compare available stock, prices, delivery time,
        and reliability where the dataset provides these details.

        Recommend the best suitable alternatives.
        Do not invent supplier information.

        Maximum 120 words.
        """,
        expected_output="Supplier alternatives with supporting data.",
        agent=supplier_agent
    )

    # TASK 3: INVENTORY ANALYSIS

    inventory_task = Task(
        description=f"""
        Analyze inventory for {product}.

        Required quantity: {quantity}

        Use the Inventory Analysis Tool.

        Identify:
        - Available stock
        - Shortage or surplus
        - Suitable warehouses
        - Possible stock allocation

        Use actual tool results only.

        Maximum 100 words.
        """,
        expected_output="Stock summary and allocation recommendation.",
        agent=inventory_agent
    )

    # TASK 4: LOGISTICS ANALYSIS

    logistics_task = Task(
        description=f"""
        Compare transport options.

        Delivery deadline: {deadline_days} days.

        Use the Logistics Comparison Tool.

        Compare cost, delivery time, and reliability.
        Identify options that meet the deadline.
        Use actual tool results only.

        Maximum 100 words.
        """,
        expected_output="Transport comparison and best option.",
        agent=logistics_agent
    )

    # TASK 5: RISK ASSESSMENT

    risk_task = Task(
        description="""
        Review the four previous agent findings.

        Evaluate:
        - Crisis severity
        - Supplier availability and reliability
        - Warehouse stock
        - Transport costs and delivery
        - Recovery risks

        Compare internal stock redistribution with
        alternative supplier sourcing.

        Identify uncertainties and the most suitable
        recovery option.

        Use only the previous findings.
        Do not repeat their full reports.

        Maximum 130 words.
        """,
        expected_output="Evidence-based risk assessment and recommendation.",
        agent=risk_agent,
        context=[
            crisis_task,
            supplier_task,
            inventory_task,
            logistics_task
        ]
    )

    # TASK 6: FINAL RECOVERY PLAN

    recovery_task = Task(
        description="""
        Prepare the final Supply Chain Crisis Recovery Plan.

        Review all five previous agent findings.

        Use these sections:

        1. Crisis Summary
        2. Risk Severity
        3. Supplier Recommendation
        4. Inventory Recovery
        5. Logistics Recommendation
        6. Immediate Actions
        7. Long-Term Prevention
        8. Missing Information and Human Approval

        Give prioritized and practical recommendations.

        Use only verified information.
        Never invent costs, quantities, or delivery times.
        Avoid repeating the same findings.

        Maximum 400 words.
        """,
        expected_output="A professional recovery plan under 400 words.",
        agent=recovery_agent,
        context=[
            crisis_task,
            supplier_task,
            inventory_task,
            logistics_task,
            risk_task
        ]
    )

    # EXECUTE CREW

    crew = Crew(
        agents=[
            crisis_agent,
            supplier_agent,
            inventory_agent,
            logistics_agent,
            risk_agent,
            recovery_agent
        ],
        tasks=[
            crisis_task,
            supplier_task,
            inventory_task,
            logistics_task,
            risk_task,
            recovery_task
        ],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    return str(result)
