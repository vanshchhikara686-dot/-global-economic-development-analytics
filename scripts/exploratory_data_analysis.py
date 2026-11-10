import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

# ==========================================
# E-COMMERCE EXPLORATORY DATA ANALYSIS
# ==========================================

START_TIME = time.time()

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CHUNK_SIZE = 100000

print("=" * 60)
print("E-COMMERCE EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nProject configuration completed!")
print("Input file:", INPUT_FILE)
print("Output folder:", OUTPUT_FOLDER)
print("Chunk size:", CHUNK_SIZE)
# ==========================================
# STEP 1: OVERALL BUSINESS KPIs
# ==========================================

print("\nCALCULATING OVERALL BUSINESS KPIs")

total_revenue = 0
total_orders = 0
total_units = 0
total_discount = 0
total_records = 0

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    total_revenue += chunk["Total_Amount"].sum()
    total_orders += chunk["Order_ID"].nunique()
    total_units += chunk["Quantity"].sum()
    total_discount += chunk["Discount"].sum()
    total_records += len(chunk)

average_order_value = total_revenue / total_orders
average_discount = total_discount / total_records

print("\n" + "=" * 50)
print("OVERALL BUSINESS PERFORMANCE")
print("=" * 50)

print(f"Total Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: Rs. {average_order_value:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Average Discount: {average_discount:.2f}%")

print("=" * 50)
# ==========================================
# STEP 2: CATEGORY-WISE SALES ANALYSIS
# ==========================================

print("\nANALYSING SALES BY CATEGORY")

category_data = {}

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Category").agg(
        Revenue=("Total_Amount", "sum"),
        Units_Sold=("Quantity", "sum"),
        Orders=("Order_ID", "nunique")
    )

    for category, row in grouped.iterrows():

        if category not in category_data:
            category_data[category] = {
                "Revenue": 0,
                "Units_Sold": 0,
                "Orders": 0
            }

        category_data[category]["Revenue"] += row["Revenue"]
        category_data[category]["Units_Sold"] += row["Units_Sold"]
        category_data[category]["Orders"] += row["Orders"]


category_df = pd.DataFrame.from_dict(
    category_data,
    orient="index"
)

category_df = category_df.sort_values(
    by="Revenue",
    ascending=False
)

print("\nCATEGORY-WISE PERFORMANCE")
print(category_df.round(2))

category_df.to_csv(
    f"{OUTPUT_FOLDER}/category_performance.csv"
)

print("\nCategory analysis saved successfully!")# ==========================================
# STEP 2: CATEGORY-WISE SALES ANALYSIS
# ==========================================

print("\nANALYSING SALES BY CATEGORY")

category_data = {}

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Category").agg(
        Revenue=("Total_Amount", "sum"),
        Units_Sold=("Quantity", "sum"),
        Orders=("Order_ID", "nunique")
    )

    for category, row in grouped.iterrows():

        if category not in category_data:
            category_data[category] = {
                "Revenue": 0,
                "Units_Sold": 0,
                "Orders": 0
            }

        category_data[category]["Revenue"] += row["Revenue"]
        category_data[category]["Units_Sold"] += row["Units_Sold"]
        category_data[category]["Orders"] += row["Orders"]


category_df = pd.DataFrame.from_dict(
    category_data,
    orient="index"
)

category_df = category_df.sort_values(
    by="Revenue",
    ascending=False
)

print("\nCATEGORY-WISE PERFORMANCE")
print(category_df.round(2))

category_df.to_csv(
    f"{OUTPUT_FOLDER}/category_performance.csv"
)

print("\nCategory analysis saved successfully!")
# ==========================================
# STEP 3: CATEGORY REVENUE VISUALISATION
# ==========================================

print("\nCREATING CATEGORY REVENUE CHART")

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.bar(
    category_df.index,
    category_df["Revenue"] / 10000000
)
for bar in plt.gca().patches:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )
plt.title(
    "Revenue by Product Category",
    fontsize=16
)

plt.xlabel("Product Category")
plt.ylabel("Revenue (₹ Crores)")

plt.xticks(rotation=25)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/category_revenue.png",
    dpi=300
)

plt.show()

print("Category revenue chart saved successfully!")