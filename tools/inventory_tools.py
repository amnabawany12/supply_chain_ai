
import pandas as pd
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INVENTORY_FILE = os.path.join(
    BASE_DIR, "data", "inventory.csv"
)


def check_inventory(product, required_quantity):

    # Load inventory dataset
    df = pd.read_csv(INVENTORY_FILE)

    # Find matching product
    stock = df[
        df["product"].str.lower() == product.lower()
    ]

    if stock.empty:
        return {
            "status": "error",
            "message": "No inventory records found."
        }

    # Calculate total available stock
    total_stock = int(stock["available_stock"].sum())

    # Calculate shortage
    shortage = max(
        0,
        required_quantity - total_stock
    )

    # Calculate extra stock
    extra_stock = max(
        0,
        total_stock - required_quantity
    )

    warehouses = []

    for _, warehouse in stock.iterrows():

        warehouses.append({
            "warehouse": warehouse["warehouse_name"],
            "location": warehouse["location"],
            "available_stock": int(
                warehouse["available_stock"]
            )
        })

    return {
        "status": "success",
        "product": product,
        "required_quantity": required_quantity,
        "total_stock": total_stock,
        "shortage": shortage,
        "extra_stock": extra_stock,
        "warehouses": warehouses
    }


def get_warehouse_stock(product):

    df = pd.read_csv(INVENTORY_FILE)

    stock = df[
        df["product"].str.lower() == product.lower()
    ]

    if stock.empty:
        return "No warehouse records found."

    return stock.to_dict(orient="records")
