
from crewai import Agent


def create_logistics_agent(llm, logistics_tool):

    return Agent(
        role="Logistics Optimization Specialist",

        goal=(
            "Compare transportation methods and recommend "
            "feasible delivery options."
        ),

        backstory=(
            "You are a logistics specialist. You evaluate "
            "transportation costs, estimated delivery times, "
            "and reliability. Only recommend options supported "
            "by the supplied transportation data."
        ),

        tools=[logistics_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
