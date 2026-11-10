
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
print("ORDER STATUS ANALYSIS")
print("=" * 55)

# ==========================================
# STEP 1: PROCESS DATA IN CHUNKS
# ==========================================

status_counts = {}

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    counts = chunk["Order_Status"].value_counts()

    for status, count in counts.items():
        status_counts[status] = (
            status_counts.get(status, 0) + count
        )

# ==========================================
# STEP 2: CREATE SUMMARY TABLE
# ==========================================

status_df = pd.DataFrame(
    list(status_counts.items()),
    columns=["Order_Status", "Total_Orders"]
)

status_df = status_df.sort_values(
    by="Total_Orders",
    ascending=False
)

total_orders = status_df["Total_Orders"].sum()

status_df["Percentage"] = (
    status_df["Total_Orders"] / total_orders
) * 100

print("\nORDER STATUS SUMMARY")
print(status_df.round(2).to_string(index=False))

# Save summary
status_df.to_csv(
    f"{OUTPUT_FOLDER}/order_status_summary.csv",
    index=False
)

# ==========================================
# STEP 3: CREATE BAR CHART
# ==========================================

print("\nCREATING ORDER STATUS CHART")

plt.figure(figsize=(10, 6))

bars = plt.bar(
    status_df["Order_Status"],
    status_df["Total_Orders"]
)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.title("Orders by Order Status", fontsize=16)
plt.xlabel("Order Status")
plt.ylabel("Number of Orders")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    f"{OUTPUT_FOLDER}/orders_by_status.png",
    dpi=300
)

plt.show()

# ==========================================
# STEP 4: BUSINESS INSIGHTS
# ==========================================

print("\nBUSINESS INSIGHTS")

for _, row in status_df.iterrows():
    print(
        f"{row['Order_Status']}: "
        f"{row['Total_Orders']:,} orders "
        f"({row['Percentage']:.2f}%)"
    )

print("\nTotal Orders:", f"{total_orders:,}")

print("\nAnalysis completed successfully!")
print(
    "Execution time:",
    round(time.time() - START_TIME, 2),
    "seconds"
)
