import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# PAYMENT METHOD ANALYSIS
# ==========================================

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CHUNK_SIZE = 100000

print("=" * 55)
print("PAYMENT METHOD ANALYSIS")
print("=" * 55)

payment_counts = {}

# Read dataset in chunks
for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Payment_Method").size()

    for method, count in grouped.items():
        payment_counts[method] = (
            payment_counts.get(method, 0) + count
        )

# Convert to DataFrame
payment_df = pd.DataFrame(
    list(payment_counts.items()),
    columns=["Payment_Method", "Total_Orders"]
)

# Sort by order count
payment_df = payment_df.sort_values(
    by="Total_Orders",
    ascending=False
)

print("\nORDERS BY PAYMENT METHOD")
print(payment_df.to_string(index=False))

# Calculate percentages
total_orders = payment_df["Total_Orders"].sum()

payment_df["Percentage"] = (
    payment_df["Total_Orders"] / total_orders
) * 100

# Save summary
payment_df.to_csv(
    f"{OUTPUT_FOLDER}/payment_method_summary.csv",
    index=False
)

# ==========================================
# CREATE VISUALISATION
# ==========================================

print("\nCREATING PAYMENT METHOD CHART")

plt.figure(figsize=(11, 6))

bars = plt.bar(
    payment_df["Payment_Method"],
    payment_df["Total_Orders"]
)

# Add order count and percentage labels
for bar, percentage in zip(
    bars, payment_df["Percentage"]
):

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:,.0f}\n({percentage:.1f}%)",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title(
    "Orders by Payment Method",
    fontsize=16
)

plt.xlabel("Payment Method", fontsize=12)
plt.ylabel("Number of Orders", fontsize=12)

plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

# Save chart
plt.savefig(
    f"{OUTPUT_FOLDER}/payment_method_analysis.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nPayment method analysis completed!")
print("Chart and summary saved successfully!")