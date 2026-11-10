import pandas as pd
import matplotlib.pyplot as plt
import os
import time

START_TIME = time.time()

# ==========================================
# PROJECT CONFIGURATION
# ==========================================

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

CHUNK_SIZE = 100000

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("=" * 60)
print("SALES CHANNEL PERFORMANCE ANALYSIS")
print("=" * 60)

# ==========================================
# STEP 1: PROCESS DATA IN CHUNKS
# ==========================================

channel_data = {}

print("\nProcessing dataset...")

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=["Order_ID", "Sales_Channel", "Total_Amount"],
    chunksize=CHUNK_SIZE
):

    chunk["Total_Amount"] = pd.to_numeric(
        chunk["Total_Amount"],
        errors="coerce"
    )

    chunk = chunk.dropna(
        subset=["Sales_Channel", "Total_Amount"]
    )

    grouped = chunk.groupby("Sales_Channel").agg(
        Revenue=("Total_Amount", "sum"),
        Orders=("Order_ID", "count")
    )

    for channel, row in grouped.iterrows():

        if channel not in channel_data:
            channel_data[channel] = {
                "Revenue": 0,
                "Orders": 0
            }

        channel_data[channel]["Revenue"] += row["Revenue"]
        channel_data[channel]["Orders"] += row["Orders"]

print("Data processing completed!")

# ==========================================
# STEP 2: CREATE PERFORMANCE TABLE
# ==========================================

channel_df = pd.DataFrame.from_dict(
    channel_data,
    orient="index"
)

channel_df.index.name = "Sales_Channel"

channel_df["Average_Order_Value"] = (
    channel_df["Revenue"] / channel_df["Orders"]
)

channel_df["Revenue_Crores"] = (
    channel_df["Revenue"] / 10000000
)

channel_df = channel_df.sort_values(
    by="Revenue",
    ascending=False
)

print("\nCHANNEL-WISE PERFORMANCE")

print(channel_df.round(2))

# Save results

channel_df.to_csv(
    f"{OUTPUT_FOLDER}/channel_performance.csv"
)

# ==========================================
# STEP 3: REVENUE BY CHANNEL
# ==========================================

print("\nCREATING CHANNEL REVENUE CHART")

plt.figure(figsize=(12, 6))

bars = plt.bar(
    channel_df.index,
    channel_df["Revenue_Crores"]
)

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title("Revenue by Sales Channel", fontsize=16)
plt.xlabel("Sales Channel")
plt.ylabel("Revenue (₹ Crores)")
plt.xticks(rotation=25)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/channel_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# STEP 4: ORDERS BY CHANNEL
# ==========================================

print("\nCREATING CHANNEL ORDERS CHART")

plt.figure(figsize=(12, 6))

bars = plt.bar(
    channel_df.index,
    channel_df["Orders"]
)

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title("Total Orders by Sales Channel", fontsize=16)
plt.xlabel("Sales Channel")
plt.ylabel("Number of Orders")
from matplotlib.ticker import StrMethodFormatter

plt.gca().yaxis.set_major_formatter(
    StrMethodFormatter('{x:,.0f}')
)
plt.xticks(rotation=25)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/channel_orders.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# STEP 5: AVERAGE ORDER VALUE BY CHANNEL
# ==========================================

print("\nCREATING AVERAGE ORDER VALUE CHART")

plt.figure(figsize=(12, 6))

bars = plt.bar(
    channel_df.index,
    channel_df["Average_Order_Value"]
)

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"₹{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title("Average Order Value by Sales Channel", fontsize=16)
plt.xlabel("Sales Channel")
plt.ylabel("Average Order Value (₹)")
plt.xticks(rotation=25)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/channel_average_order_value.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# STEP 6: BUSINESS INSIGHTS
# ==========================================

best_revenue_channel = channel_df["Revenue"].idxmax()

best_order_channel = channel_df["Orders"].idxmax()

best_aov_channel = channel_df["Average_Order_Value"].idxmax()

print("\n" + "=" * 60)
print("KEY BUSINESS INSIGHTS")
print("=" * 60)

print("Highest Revenue Channel:", best_revenue_channel)

print("Highest Order Volume Channel:", best_order_channel)

print("Highest Average Order Value Channel:", best_aov_channel)

print("\nAnalysis completed!")

print(
    "Execution time:",
    round(time.time() - START_TIME, 2),
    "seconds"
)
# ==========================================
# STEP 6: BUSINESS INSIGHTS
# ==========================================

print("\n" + "=" * 55)
print("BUSINESS INSIGHTS - SALES CHANNEL PERFORMANCE")
print("=" * 55)

# Best performing channels
best_revenue_channel = channel_df["Revenue"].idxmax()
best_order_channel = channel_df["Orders"].idxmax()
best_aov_channel = channel_df["Average_Order_Value"].idxmax()

# Display insights
print("\n1. HIGHEST REVENUE CHANNEL")
print("Channel:", best_revenue_channel)
print("Revenue: Rs.", round(
    channel_df.loc[best_revenue_channel, "Revenue"], 2
))

print("\n2. HIGHEST ORDER VOLUME CHANNEL")
print("Channel:", best_order_channel)
print("Orders:", int(
    channel_df.loc[best_order_channel, "Orders"]
))

print("\n3. HIGHEST AVERAGE ORDER VALUE CHANNEL")
print("Channel:", best_aov_channel)
print("AOV: Rs.", round(
    channel_df.loc[best_aov_channel, "Average_Order_Value"], 2
))

print("\n" + "=" * 55)
print("BUSINESS INSIGHTS COMPLETED")
print("=" * 55)