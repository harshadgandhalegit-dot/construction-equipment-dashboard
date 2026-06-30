"""
data_cleaning.py
-----------------
Cleans and transforms raw construction equipment sales data
before loading into Power BI for the Division Performance Dashboard.

Tools: Python, Pandas, NumPy
"""

import pandas as pd
import numpy as np

# 1. Load raw data
df = pd.read_csv("../data/equipment_sales_sample.csv")

# 2. Basic cleaning
df["Date"] = pd.to_datetime(df["Date"])
df.dropna(subset=["Units_Sold", "Revenue_INR", "Cost_INR"], inplace=True)
df["Division"] = df["Division"].str.strip().str.title()
df["Region"] = df["Region"].str.strip().str.title()

# 3. Feature engineering
df["Profit_INR"] = df["Revenue_INR"] - df["Cost_INR"]
df["Profit_Margin_%"] = np.round((df["Profit_INR"] / df["Revenue_INR"]) * 100, 2)
df["Avg_Revenue_Per_Unit"] = np.round(df["Revenue_INR"] / df["Units_Sold"], 2)
df["Month"] = df["Date"].dt.to_period("M").astype(str)
df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)

# 4. Data validation checks
assert (df["Units_Sold"] > 0).all(), "Found rows with zero or negative units sold"
assert (df["Revenue_INR"] >= df["Cost_INR"]).all(), "Found rows where cost exceeds revenue"

# 5. Division-wise summary (used for KPI cards in Power BI)
division_summary = (
    df.groupby("Division")
    .agg(
        Total_Units=("Units_Sold", "sum"),
        Total_Revenue=("Revenue_INR", "sum"),
        Total_Profit=("Profit_INR", "sum"),
        Avg_Margin=("Profit_Margin_%", "mean"),
    )
    .round(2)
    .reset_index()
    .sort_values("Total_Revenue", ascending=False)
)

# 6. Export cleaned data for Power BI
df.to_csv("../data/equipment_sales_cleaned.csv", index=False)
division_summary.to_csv("../data/division_summary.csv", index=False)

print("Data cleaning complete.")
print(division_summary)
