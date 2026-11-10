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
print("MONTHLY REVENUE TREND ANALYSIS")
print("=" * 60)

# ==========================================
# STEP 1: PROCESS DATA IN CHUNKS
# ==========================================

monthly_revenue = {}

print("\nProcessing dataset...")

for chunk in pd.read_csv(
    INPUT_FILE,
    usecols=["Order_Date", "Total_Amount"],
    chunksize=CHUNK_SIZE
):

    chunk["Order_Date"] = pd.to_datetime(
        chunk["Order_Date"],
        errors="coerce"
    )

    chunk["Total_Amount"] = pd.to_numeric(
        chunk["Total_Amount"],
        errors="coerce"
    )

    chunk = chunk.dropna(
        subset=["Order_Date", "Total_Amount"]
    )

    chunk["Month"] = (
        chunk["Order_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_data = chunk.groupby(
        "Month"
    )["Total_Amount"].sum()

    for month, revenue in monthly_data.items():

        monthly_revenue[month] = (
            monthly_revenue.get(month, 0) + revenue
        )

print("Data processing completed!")

# ==========================================
# STEP 2: CREATE MONTHLY DATAFRAME
# ==========================================

monthly_df = pd.Series(
    monthly_revenue,
    name="Revenue"
).sort_index().to_frame()

monthly_df["Revenue_Crores"] = (
    monthly_df["Revenue"] / 10000000
)

print("\nMONTHLY REVENUE SUMMARY")
print(monthly_df.round(2))

# Save monthly summary

monthly_df.to_csv(
    f"{OUTPUT_FOLDER}/monthly_revenue.csv"
)

# ==========================================
# STEP 3: CREATE REVENUE TREND CHART
# ==========================================

print("\nCREATING MONTHLY REVENUE CHART")

plt.figure(figsize=(16, 7))

plt.plot(
    monthly_df.index,
    monthly_df["Revenue_Crores"],
    marker="o",
    linewidth=2,
    markersize=5
)

plt.title(
    "Monthly Revenue Trend (2021–2025)",
    fontsize=17
)

plt.xlabel("Month", fontsize=12)

plt.ylabel(
    "Revenue (₹ Crores)",
    fontsize=12
)

plt.xticks(
    rotation=60,
    fontsize=8
)

# Add revenue labels every 3 months

for i in range(0, len(monthly_df), 3):

    month = monthly_df.index[i]

    revenue = monthly_df["Revenue_Crores"].iloc[i]

    plt.annotate(
        f"{revenue:,.0f}",
        (month, revenue),
        textcoords="offset points",
        xytext=(0, 10),
        ha="center",
        fontsize=8
    )

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

# Save chart

plt.savefig(
    f"{OUTPUT_FOLDER}/monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# STEP 4: IDENTIFY BEST AND WORST MONTHS
# ==========================================

best_month = monthly_df["Revenue_Crores"].idxmax()

worst_month = monthly_df["Revenue_Crores"].idxmin()

print("\nREVENUE INSIGHTS")

print(
    "Highest Revenue Month:",
    best_month
)

print(
    "Highest Revenue:",
    round(monthly_df.loc[best_month, "Revenue_Crores"], 2),
    "Crores"
)

print(
    "Lowest Revenue Month:",
    worst_month
)

print(
    "Lowest Revenue:",
    round(monthly_df.loc[worst_month, "Revenue_Crores"], 2),
    "Crores"
)

print("\nMonthly analysis completed!")

print(
    "Execution time:",
    round(time.time() - START_TIME, 2),
    "seconds"
)