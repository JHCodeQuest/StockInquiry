#Inventory related helpers

from utils.csv_handler import save_csv
from utils.fake_thinking import simulate_thinking


def process_inventory_data():
    print("Starting inventory processing...")
    simulate_thinking(2, "Loading stock info...")
    simulate_thinking(3, "Formatting data...")

    data = [
        {"Item": "Widget A", "Qty": 10, "Location": "Store 01"},
        {"Item": "Widget B", "Qty": 5, "Location": "Store 02"}
    ]

    save_csv(data, "inventory_data.csv")
    print("✅ Inventory data processed and saved to inventory_data.csv")