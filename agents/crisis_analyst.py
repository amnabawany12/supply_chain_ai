
from crewai import Agent


def create_crisis_analyst(llm):

    return Agent(
        role="Supply Chain Crisis Analyst",

        goal=(
            "Analyze supply chain disruptions, identify "
            "their causes, and classify their severity."
        ),

        backstory=(
            "You are an experienced supply chain analyst. "
            "You investigate shipment delays, supplier failures, "
            "and inventory problems. You must use the provided "
            "information and never invent missing facts."
        ),

        llm=llm,
        verbose=True,
        allow_delegation=False
    )
