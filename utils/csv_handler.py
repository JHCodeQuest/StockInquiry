#save/read csv files

import csv


def save_csv(data, filename):
    if not data:
        print("No data to save.")
        return

    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"File saved: {filename}")