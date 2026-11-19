
from crewai import Agent


def create_recovery_manager(llm):

    return Agent(
        role="Supply Chain Recovery Manager",

        goal=(
            "Combine all agent findings and generate "
            "a practical, prioritized crisis recovery plan."
        ),

        backstory=(
            "You are a senior supply chain recovery manager. "
            "You receive reports from crisis, supplier, inventory, "
            "logistics, and risk specialists. You coordinate their "
            "findings and prepare a clear final recovery strategy. "
            "Never invent prices, availability, or delivery times."
        ),

        llm=llm,
        verbose=True,
        allow_delegation=False
    )
