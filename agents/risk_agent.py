
from crewai import Agent


def create_risk_agent(llm):

    return Agent(
        role="Supply Chain Risk Assessment Specialist",

        goal=(
            "Evaluate possible recovery solutions and compare "
            "their costs, delivery times, and operational risks."
        ),

        backstory=(
            "You are a risk assessment specialist. "
            "You examine the findings of other agents, identify "
            "weaknesses, compare alternatives, and explain "
            "the risks of each proposed decision."
        ),

        llm=llm,
        verbose=True,
        allow_delegation=False
    )
