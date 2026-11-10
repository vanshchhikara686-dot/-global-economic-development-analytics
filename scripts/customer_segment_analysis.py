
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

START_TIME = time.time()

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

CHUNK_SIZE = 100000

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("=" * 55)
print("CUSTOMER SEGMENT ANALYSIS")
print("=" * 55)

# ==========================================
# STEP 1: PROCESS DATA IN CHUNKS
# ==========================================

segment_data = pd.DataFrame()

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Customer_Segment").agg(
        Revenue=("Total_Amount", "sum"),
        Orders=("Order_ID", "count"),
        Units_Sold=("Quantity", "sum")
    )

    if segment_data.empty:
        segment_data = grouped
    else:
        segment_data = segment_data.add(grouped, fill_value=0)

# ==========================================
# STEP 2: CALCULATE AVERAGE ORDER VALUE
# ==========================================

segment_data["Average_Order_Value"] = (
    segment_data["Revenue"] / segment_data["Orders"]
)

segment_data = segment_data.sort_values(
    by="Revenue",
    ascending=False
)

print("\nCUSTOMER SEGMENT PERFORMANCE")
print(segment_data.round(2))

# Save results
segment_data.to_csv(
    f"{OUTPUT_FOLDER}/customer_segment_performance.csv"
)

# ==========================================
# STEP 3: CREATE REVENUE CHART
# ==========================================

print("\nCREATING CUSTOMER SEGMENT REVENUE CHART")

plt.figure(figsize=(10, 6))

bars = plt.bar(
    segment_data.index,
    segment_data["Revenue"] / 10000000
)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"₹{height:,.0f} Cr",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.title("Revenue by Customer Segment", fontsize=16)
plt.xlabel("Customer Segment")
plt.ylabel("Revenue (₹ Crores)")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/revenue_by_customer_segment.png",
    dpi=300
)

plt.show()

# ==========================================
# STEP 4: BUSINESS INSIGHTS
# ==========================================

best_segment = segment_data["Revenue"].idxmax()

print("\nBUSINESS INSIGHTS")
print("Highest revenue segment:", best_segment)

print(
    "Revenue generated: ₹",
    round(segment_data.loc[best_segment, "Revenue"], 2)
)

print("\nAnalysis completed successfully!")

print("Execution time:", round(time.time() - START_TIME, 2), "seconds")

