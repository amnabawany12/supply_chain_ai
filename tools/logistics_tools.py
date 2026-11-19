
import pandas as pd


# Sample transportation options for demonstration
TRANSPORT_OPTIONS = [
    {
        "mode": "Road Transport",
        "cost": 12000,
        "delivery_days": 5,
        "reliability": 90
    },
    {
        "mode": "Air Transport",
        "cost": 25000,
        "delivery_days": 2,
        "reliability": 97
    },
    {
        "mode": "Rail Transport",
        "cost": 9000,
        "delivery_days": 7,
        "reliability": 85
    }
]


def compare_transport_options(deadline_days):

    df = pd.DataFrame(TRANSPORT_OPTIONS)

    feasible = df[
        df["delivery_days"] <= deadline_days
    ]

    if feasible.empty:
        return {
            "message": "No transportation option meets the required deadline.",
            "available_options": TRANSPORT_OPTIONS
        }

    feasible = feasible.sort_values(
        by=["cost", "reliability"],
        ascending=[True, False]
    )

    return feasible.to_dict(orient="records")
