
from crewai import Agent


def create_inventory_agent(llm, inventory_tool):

    return Agent(
        role="Inventory Management Analyst",

        goal=(
            "Analyze warehouse inventory and calculate "
            "product shortages and available stock."
        ),

        backstory=(
            "You are an inventory management expert. "
            "You examine warehouse records, calculate shortages, "
            "and recommend stock redistribution when possible."
        ),

        tools=[inventory_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
