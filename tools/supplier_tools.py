
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVENTORY_FILE = os.path.join(BASE_DIR, "data", "inventory.csv")


def check_inventory(product, required_quantity):

    df = pd.read_csv(INVENTORY_FILE)

    stock = df[
        df["product"].astype(str).str.strip().str.lower()
        == product.strip().lower()
    ]

    if stock.empty:
        return "No inventory records found for this product."

    total_stock = int(stock["available_stock"].sum())

    shortage = max(0, required_quantity - total_stock)

    warehouses = []

    for _, row in stock.iterrows():
        warehouses.append({
            "warehouse": row["warehouse_name"],
            "location": row["location"],
            "available_stock": int(row["available_stock"])
        })

    return {
        "product": product,
        "required_quantity": required_quantity,
        "total_stock": total_stock,
        "shortage": shortage,
        "warehouses": warehouses
    }


def find_alternative_suppliers(product, required_quantity):

    df = pd.read_csv(INVENTORY_FILE)

    stock = df[
        df["product"].astype(str).str.strip().str.lower()
        == product.strip().lower()
    ]

    if stock.empty:
        return "No alternative warehouse inventory found."

    total_stock = int(stock["available_stock"].sum())

    warehouses = []

    for _, row in stock.iterrows():

        warehouses.append({
            "warehouse": row["warehouse_name"],
            "location": row["location"],
            "available_stock": int(row["available_stock"])
        })

    if total_stock >= required_quantity:

        return {
            "status": "sufficient_stock",
            "product": product,
            "required_quantity": required_quantity,
            "total_available_stock": total_stock,
            "warehouses": warehouses,
            "recommendation": "Sufficient stock is available across the listed warehouses."
        }

    return {
        "status": "insufficient_stock",
        "product": product,
        "required_quantity": required_quantity,
        "total_available_stock": total_stock,
        "shortage": required_quantity - total_stock,
        "warehouses": warehouses,
        "recommendation": "Additional stock is required."
    }
