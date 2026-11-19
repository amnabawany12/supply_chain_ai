
from crewai import Agent


def create_supplier_agent(llm, supplier_tool):

    return Agent(
        role="Alternative Supplier Researcher",

        goal=(
            "Find reliable alternative suppliers by checking "
            "availability, prices, reliability, and delivery time."
        ),

        backstory=(
            "You are a supplier research specialist. "
            "You compare supplier records and recommend "
            "the best available alternatives using actual data."
        ),

        tools=[supplier_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
