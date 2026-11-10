import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "cleaned" / "worldbank_global_cleaned.csv"

CHART_DIR = BASE_DIR / "outputs" / "charts" / "agriculture"

CHART_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD DATA
# ==========================================

print("\nLoading World Bank dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")
print("Total records:", len(df))

# ==========================================
# 3. SELECT AGRICULTURE INDICATORS
# ==========================================

agriculture = df[
    df["Indicator_Category"].isin([
        "Agriculture_GDP",
        "Agriculture_Employment",
        "Cereal_Yield"
    ])
].copy()

print("\nAgriculture records:", len(agriculture))

# ==========================================
# 4. DATA PREPARATION
# ==========================================

agriculture["Value"] = pd.to_numeric(
    agriculture["Value"],
    errors="coerce"
)

agriculture.dropna(subset=["Value"], inplace=True)

# ==========================================
# 5. AGRICULTURE GDP TREND
# ==========================================

print("\nAnalysing agriculture contribution to GDP...")

ag_gdp = agriculture[
    agriculture["Indicator_Category"] == "Agriculture_GDP"
]

gdp_trend = (
    ag_gdp.groupby("Year")["Value"]
    .mean()
)

plt.figure(figsize=(12, 6))

plt.plot(
    gdp_trend.index,
    gdp_trend.values,
    marker="o",
    linewidth=2
)

plt.title(
    "Average Agriculture Value Added (% of GDP), 2000–2024",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Agriculture Value Added (%)")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "agriculture_gdp_trend.png",
    dpi=300
)

plt.show()
plt.close()

# ==========================================
# 6. AGRICULTURAL EMPLOYMENT TREND
# ==========================================

print("\nAnalysing agricultural employment...")

ag_employment = agriculture[
    agriculture["Indicator_Category"] == "Agriculture_Employment"
]

employment_trend = (
    ag_employment.groupby("Year")["Value"]
    .mean()
)

plt.figure(figsize=(12, 6))

plt.plot(
    employment_trend.index,
    employment_trend.values,
    marker="o",
    linewidth=2
)

plt.title(
    "Average Agricultural Employment (% of Total Employment), 2000–2024",
    fontsize=14,
    fontweight="bold"
)

plt.xlabel("Year")
plt.ylabel("Agricultural Employment (%)")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "agricultural_employment_trend.png",
    dpi=300
)

plt.show()
plt.close()

# ==========================================
# 7. TOP 10 COUNTRIES BY CEREAL YIELD
# ==========================================

print("\nAnalysing cereal yield...")

cereal = agriculture[
    agriculture["Indicator_Category"] == "Cereal_Yield"
]

latest_cereal = cereal[
    cereal["Year"] == cereal["Year"].max()
]

top_cereal = (
    latest_cereal.groupby("Country_Name")["Value"]
    .mean()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(12, 7))

top_cereal.plot(kind="barh")

plt.title(
    "Top 10 Countries by Cereal Yield",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel("Cereal Yield (kg per hectare)")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_10_cereal_yield.png",
    dpi=300
)

plt.show()
plt.close()

# ==========================================
# 8. AGRICULTURE GDP VS EMPLOYMENT
# ==========================================

print("\nAnalysing agriculture GDP vs employment...")

gdp_latest = ag_gdp.sort_values("Year").groupby(
    "Country_Code"
).tail(1)

employment_latest = ag_employment.sort_values("Year").groupby(
    "Country_Code"
).tail(1)

comparison = pd.merge(
    gdp_latest[["Country_Code", "Country_Name", "Value"]],
    employment_latest[["Country_Code", "Value"]],
    on="Country_Code",
    suffixes=("_GDP", "_Employment")
)

comparison.dropna(inplace=True)

plt.figure(figsize=(10, 7))

plt.scatter(
    comparison["Value_Employment"],
    comparison["Value_GDP"],
    alpha=0.6
)

plt.title(
    "Agricultural Employment vs Agriculture's GDP Contribution",
    fontsize=13,
    fontweight="bold"
)

plt.xlabel("Agricultural Employment (%)")
plt.ylabel("Agriculture Value Added (% of GDP)")

plt.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "agriculture_gdp_vs_employment.png",
    dpi=300
)

plt.show()
plt.close()

# ==========================================
# 9. SAVE ANALYSIS DATA
# ==========================================

comparison.to_csv(
    BASE_DIR / "data" / "processed" /
    "agriculture_gdp_employment_comparison.csv",
    index=False
)

print("\n====================================")
print("AGRICULTURE ANALYSIS COMPLETED")
print("====================================")

print("Agriculture GDP records:", len(ag_gdp))
print("Agricultural employment records:", len(ag_employment))
print("Cereal yield records:", len(cereal))

print("\nCharts saved in:")
print(CHART_DIR)

print("\nAnalysis completed successfully!")