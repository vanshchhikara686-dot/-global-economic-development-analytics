import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# TOP 10 PRODUCTS BY REVENUE
# ==========================================

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CHUNK_SIZE = 100000

print("=" * 55)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 55)

product_revenue = {}

# Process dataset in chunks
for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    grouped = chunk.groupby("Product_Name")["Total_Amount"].sum()

    for product, revenue in grouped.items():

        product_revenue[product] = (
            product_revenue.get(product, 0) + revenue
        )

# Convert to DataFrame
product_df = pd.DataFrame(
    list(product_revenue.items()),
    columns=["Product_Name", "Revenue"]
)

# Exclude Unknown products
product_df = product_df[
    product_df["Product_Name"] != "Unknown"
]

# Select top 10
top_products = product_df.sort_values(
    by="Revenue",
    ascending=False
).head(10)

print("\nTOP 10 PRODUCTS BY REVENUE")
print(top_products.round(2).to_string(index=False))

# Save CSV
top_products.to_csv(
    f"{OUTPUT_FOLDER}/top_10_products_revenue.csv",
    index=False
)

# ==========================================
# CREATE CHART
# ==========================================

plt.figure(figsize=(12, 7))

bars = plt.barh(
    top_products["Product_Name"],
    top_products["Revenue"] / 10000000
)

# Highest revenue at the top
plt.gca().invert_yaxis()

# Add labels
for bar in bars:

    width = bar.get_width()

    plt.text(
        width,
        bar.get_y() + bar.get_height() / 2,
        f"₹{width:,.2f} Cr",
        va="center",
        fontsize=9
    )

plt.title(
    "Top 10 Products by Revenue",
    fontsize=16
)

plt.xlabel("Revenue (₹ Crores)")
plt.ylabel("Product Name")

plt.grid(axis="x", linestyle="--", alpha=0.4)

plt.tight_layout()

# Save chart
plt.savefig(
    f"{OUTPUT_FOLDER}/top_10_products_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nTop product analysis completed!")
print("Chart and report saved successfully!")