import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# AVERAGE ORDER VALUE BY CUSTOMER SEGMENT
# ==========================================

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CHUNK_SIZE = 100000

print("=" * 55)
print("AVERAGE ORDER VALUE BY CUSTOMER SEGMENT")
print("=" * 55)

segment_revenue = {}
segment_orders = {}

# Process dataset in chunks
for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Customer_Segment").agg(
        Revenue=("Total_Amount", "sum"),
        Orders=("Order_ID", "count")
    )

    for segment, row in grouped.iterrows():

        segment_revenue[segment] = (
            segment_revenue.get(segment, 0) + row["Revenue"]
        )

        segment_orders[segment] = (
            segment_orders.get(segment, 0) + row["Orders"]
        )

# Create DataFrame
segment_df = pd.DataFrame({
    "Customer_Segment": list(segment_revenue.keys()),
    "Revenue": list(segment_revenue.values()),
    "Orders": [
        segment_orders[s] for s in segment_revenue.keys()
    ]
})

# Calculate AOV
segment_df["Average_Order_Value"] = (
    segment_df["Revenue"] / segment_df["Orders"]
)

segment_df = segment_df.sort_values(
    "Average_Order_Value",
    ascending=False
)

print("\nAVERAGE ORDER VALUE BY CUSTOMER SEGMENT")
print(segment_df.round(2).to_string(index=False))

# Save results
segment_df.to_csv(
    f"{OUTPUT_FOLDER}/segment_aov_summary.csv",
    index=False
)

# ==========================================
# CREATE CHART
# ==========================================

plt.figure(figsize=(11, 6))

bars = plt.bar(
    segment_df["Customer_Segment"],
    segment_df["Average_Order_Value"]
)

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"₹{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.title(
    "Average Order Value by Customer Segment",
    fontsize=16
)

plt.xlabel("Customer Segment")
plt.ylabel("Average Order Value (₹)")

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/segment_aov_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nSegment AOV analysis completed!")
print("Chart and summary saved successfully!")