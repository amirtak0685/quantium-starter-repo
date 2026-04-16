"""Combine daily_sales_data_*.csv into one file: Pink Morsels only, Sales = quantity * price."""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
SOURCES = [
    DATA / "daily_sales_data_0.csv",
    DATA / "daily_sales_data_1.csv",
    DATA / "daily_sales_data_2.csv",
]
OUTPUT = DATA / "formatted_output.csv"


def main() -> None:
    frames = [pd.read_csv(p) for p in SOURCES]
    df = pd.concat(frames, ignore_index=True)
    pink = df[df["product"].str.lower().str.strip() == "pink morsel"].copy()
    price = pink["price"].str.replace("$", "", regex=False).astype(float)
    pink["Sales"] = pink["quantity"] * price
    out = pink.rename(columns={"date": "Date", "region": "Region"})[
        ["Sales", "Date", "Region"]
    ]
    out.to_csv(OUTPUT, index=False)


if __name__ == "__main__":
    main()
