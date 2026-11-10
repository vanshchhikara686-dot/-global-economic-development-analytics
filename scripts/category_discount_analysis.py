import pandas as pd
import matplotlib.pyplot as plt
import os
import time

# ==========================================
# CATEGORY-WISE DISCOUNT ANALYSIS
# ==========================================

START_TIME = time.time()

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/category_discount"

CHUNK_SIZE = 100000

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

print("=" * 60)
print("CATEGORY-WISE DISCOUNT ANALYSIS")
print("=" * 60)

# ==========================================
# STEP 1: INITIALISE SUMMARY
# ==========================================

category_summary = {}

print("\nReading dataset in chunks...")

# ==========================================
# STEP 2: PROCESS DATA
# ==========================================

for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Category").agg(
        Revenue=("Total_Amount", "sum"),
        Orders=("Order_ID", "nunique"),
        Units_Sold=("Quantity", "sum"),
        Discount_Sum=("Discount", "sum"),
        Discount_Count=("Discount", "count")
    )

    for category, row in grouped.iterrows():

        if category not in category_summary:
            category_summary[category] = {
                "Revenue": 0,
                "Orders": 0,
                "Units_Sold": 0,
                "Discount_Sum": 0,
                "Discount_Count": 0
            }

        category_summary[category]["Revenue"] += row["Revenue"]
        category_summary[category]["Orders"] += row["Orders"]
        category_summary[category]["Units_Sold"] += row["Units_Sold"]
        category_summary[category]["Discount_Sum"] += row["Discount_Sum"]
        category_summary[category]["Discount_Count"] += row["Discount_Count"]

print("\nDataset processing completed!")

# ==========================================
# STEP 3: CREATE SUMMARY DATAFRAME
# ==========================================

category_df = pd.DataFrame.from_dict(
    category_summary,
    orient="index"
)

category_df.index.name = "Category"

category_df["Average_Discount"] = (
    category_df["Discount_Sum"] /
    category_df["Discount_Count"]
)

category_df = category_df.drop(
    columns=["Discount_Sum", "Discount_Count"]
)

category_df = category_df.sort_values(
    by="Revenue",
    ascending=False
)

print("\nCATEGORY-WISE PERFORMANCE")
print(category_df.round(2))

# ==========================================
# STEP 4: SAVE SUMMARY
# ==========================================

SUMMARY_FILE = os.path.join(
    OUTPUT_FOLDER,
    "category_discount_summary.csv"
)

category_df.to_csv(SUMMARY_FILE)

print("\nSummary saved successfully!")

# ==========================================
# STEP 5: REVENUE CHART
# ==========================================

print("\nCreating category revenue chart...")

plt.figure(figsize=(12, 6))

bars = plt.bar(
    category_df.index,
    category_df["Revenue"] / 10000000
)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"₹{height:,.0f} Cr",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title("Revenue by Product Category", fontsize=16)
plt.xlabel("Product Category")
plt.ylabel("Revenue (₹ Crores)")
plt.xticks(rotation=25)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "category_revenue.png"),
    dpi=300
)

plt.show()

# ==========================================
# STEP 6: DISCOUNT CHART
# ==========================================

print("\nCreating category discount chart...")

plt.figure(figsize=(12, 6))

bars = plt.bar(
    category_df.index,
    category_df["Average_Discount"]
)

for bar in bars:
    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"{height:.2f}%",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title("Average Discount by Product Category", fontsize=16)
plt.xlabel("Product Category")
plt.ylabel("Average Discount (%)")
plt.xticks(rotation=25)
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_FOLDER, "category_discount.png"),
    dpi=300
)

plt.show()

# ==========================================
# STEP 7: COMPLETION
# ==========================================

print("\n" + "=" * 60)
print("CATEGORY DISCOUNT ANALYSIS COMPLETED")
print("=" * 60)

print("Summary:", SUMMARY_FILE)
print("Charts saved in:", OUTPUT_FOLDER)

print(f"Execution time: {time.time() - START_TIME:.2f} seconds")

