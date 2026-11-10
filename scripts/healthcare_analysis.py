import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# =====================================================
# 1. PROJECT CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "worldbank_global_cleaned.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs"
CHART_DIR = OUTPUT_DIR / "charts"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

CHART_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

HEALTHCARE_INDICATOR = "Health_Expenditure"
LIFE_INDICATOR = "Life_Expectancy"

# =====================================================
# 2. LOAD DATA
# =====================================================

print("\nLoading World Bank dataset...")

df = pd.read_csv(INPUT_FILE)

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

print("Dataset loaded successfully!")
print("Total records:", len(df))

# =====================================================
# 3. PREPARE HEALTHCARE DATA
# =====================================================

health = df[
    df["Indicator_Category"] == HEALTHCARE_INDICATOR
].copy()

health = health.dropna(subset=["Value", "Year"])

health["Year"] = health["Year"].astype(int)

health = health[
    (health["Value"] >= 0) &
    (health["Value"] <= 100)
]

print("\nHealthcare expenditure records:", len(health))

# =====================================================
# 4. PREPARE LIFE EXPECTANCY DATA
# =====================================================

life = df[
    df["Indicator_Category"] == LIFE_INDICATOR
].copy()

life = life.dropna(subset=["Value", "Year"])

life["Year"] = life["Year"].astype(int)

life = life[
    (life["Value"] > 0) &
    (life["Value"] <= 100)
]

print("Life expectancy records:", len(life))

# =====================================================
# 5. HEALTHCARE EXPENDITURE TREND
# =====================================================

print("\nAnalysing healthcare expenditure trend...")

health_trend = (
    health.groupby("Year")["Value"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12, 6))

plt.plot(
    health_trend["Year"],
    health_trend["Value"],
    marker="o",
    linewidth=2
)

plt.title(
    "Average Healthcare Expenditure (% of GDP), 2000–2024",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Healthcare Expenditure (% of GDP)")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "healthcare_expenditure_trend.png",
    dpi=300
)

plt.show()

health_trend.to_csv(
    PROCESSED_DIR / "healthcare_expenditure_trend.csv",
    index=False
)

print("Healthcare expenditure trend saved!")

# =====================================================
# 6. LIFE EXPECTANCY TREND
# =====================================================

print("\nAnalysing life expectancy trend...")

life_trend = (
    life.groupby("Year")["Value"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12, 6))

plt.plot(
    life_trend["Year"],
    life_trend["Value"],
    marker="o",
    linewidth=2
)

plt.title(
    "Average Life Expectancy Across Economies (2000–2024)",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Life Expectancy (Years)")
plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "life_expectancy_trend.png",
    dpi=300
)

plt.show()

life_trend.to_csv(
    PROCESSED_DIR / "life_expectancy_trend.csv",
    index=False
)

print("Life expectancy trend saved!")

# =====================================================
# 7. HEALTHCARE EXPENDITURE VS LIFE EXPECTANCY
# =====================================================

print("\nAnalysing healthcare expenditure vs life expectancy...")

health_life = pd.merge(
    health[
        ["Country_Code", "Country_Name", "Year", "Value"]
    ],
    life[
        ["Country_Code", "Country_Name", "Year", "Value"]
    ],
    on=["Country_Code", "Country_Name", "Year"],
    suffixes=("_Healthcare", "_Life")
)

health_life = health_life.dropna()

if len(health_life) >= 10:

    latest_common_year = (
        health_life.groupby("Year")
        .size()
        .loc[lambda x: x >= 10]
        .index.max()
    )

    comparison = health_life[
        health_life["Year"] == latest_common_year
    ].copy()

    correlation = comparison[
        ["Value_Healthcare", "Value_Life"]
    ].corr().iloc[0, 1]

    plt.figure(figsize=(10, 6))

    plt.scatter(
        comparison["Value_Healthcare"],
        comparison["Value_Life"],
        alpha=0.65
    )

    plt.title(
        f"Healthcare Expenditure vs Life Expectancy ({latest_common_year})",
        fontsize=14,
        fontweight="bold"
    )

    plt.xlabel("Healthcare Expenditure (% of GDP)")
    plt.ylabel("Life Expectancy (Years)")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "healthcare_vs_life_expectancy.png",
        dpi=300
    )

    plt.show()

    comparison.to_csv(
        PROCESSED_DIR / "healthcare_life_expectancy_comparison.csv",
        index=False
    )

    print("Comparison year:", latest_common_year)
    print("Countries compared:", len(comparison))
    print("Correlation:", round(correlation, 3))

else:
    print("Not enough matching country-year records for comparison.")

# =====================================================
# 8. TOP 10 COUNTRIES BY HEALTHCARE EXPENDITURE
# =====================================================

print("\nFinding top 10 countries by healthcare expenditure...")

latest_health = (
    health.sort_values("Year")
    .groupby("Country_Code", as_index=False)
    .tail(1)
)

top_10_health = (
    latest_health
    .sort_values("Value", ascending=False)
    .head(10)
    .sort_values("Value")
)

print("\nTOP 10 COUNTRIES BY HEALTHCARE EXPENDITURE")

print(
    top_10_health[
        ["Country_Name", "Year", "Value"]
    ].to_string(index=False)
)

plt.figure(figsize=(11, 7))

plt.barh(
    top_10_health["Country_Name"],
    top_10_health["Value"]
)

plt.title(
    "Top 10 Economies by Healthcare Expenditure",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Healthcare Expenditure (% of GDP)")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_10_healthcare_expenditure.png",
    dpi=300
)

plt.show()

top_10_health.to_csv(
    PROCESSED_DIR / "top_10_healthcare_expenditure.csv",
    index=False
)

# =====================================================
# 9. FINAL SUMMARY
# =====================================================

print("\n============================================")
print("HEALTHCARE ANALYSIS COMPLETED SUCCESSFULLY")
print("============================================")

print("Healthcare records:", len(health))
print("Life expectancy records:", len(life))

print("\nCharts saved in:")
print(CHART_DIR)

print("\nProcessed datasets saved in:")
print(PROCESSED_DIR)