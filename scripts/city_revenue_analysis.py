import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# CITY-WISE REVENUE ANALYSIS
# ==========================================

INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
OUTPUT_FOLDER = "outputs/eda"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

CHUNK_SIZE = 100000

print("=" * 55)
print("CITY-WISE REVENUE ANALYSIS")
print("=" * 55)

# Store revenue by city
city_revenue = {}

# Read dataset in chunks
for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE):

    # Group revenue by city
    grouped = chunk.groupby("City")["Total_Amount"].sum()

    # Add revenue to dictionary
    for city, revenue in grouped.items():

        city_revenue[city] = (
            city_revenue.get(city, 0) + revenue
        )

print("\nCity revenue calculation completed!")

# Convert dictionary into DataFrame
city_df = pd.DataFrame(
    list(city_revenue.items()),
    columns=["City", "Revenue"]
)

# Remove Unknown city
city_df = city_df[city_df["City"] != "Unknown"]

# Sort and select top 10
top_cities = city_df.sort_values(
    by="Revenue",
    ascending=False
).head(10)

print("\nTOP 10 CITIES BY REVENUE")
print(top_cities.round(2))

# Save results
top_cities.to_csv(
    f"{OUTPUT_FOLDER}/top_10_cities_revenue.csv",
    index=False
)

# ==========================================
# CREATE VISUALISATION
# ==========================================

print("\nCREATING CITY REVENUE CHART")

plt.figure(figsize=(12, 7))

bars = plt.bar(
    top_cities["City"],
    top_cities["Revenue"] / 10000000
)

# Add labels
for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        f"₹{height:,.1f} Cr",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.title(
    "Top 10 Cities by Revenue",
    fontsize=16
)

plt.xlabel("City", fontsize=12)
plt.ylabel("Revenue (₹ Crores)", fontsize=12)

plt.xticks(rotation=35, ha="right")

plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()

# Save chart
plt.savefig(
    f"{OUTPUT_FOLDER}/top_10_cities_revenue.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCity revenue analysis completed!")
print("Chart and report saved successfully!")