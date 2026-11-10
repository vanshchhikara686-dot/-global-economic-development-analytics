
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR / "data" / "cleaned"
    / "worldbank_global_cleaned.csv"
)

CHART_DIR = BASE_DIR / "outputs" / "charts"

CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# 2. LOAD DATASET
# ==========================================

print("Loading cleaned World Bank dataset...")

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!")

print("Total records:", len(df))

print("Countries:", df["Country_Code"].nunique())

print("Indicators:", df["Indicator_Category"].nunique())

print("Year range:", df["Year"].min(), "-", df["Year"].max())

# ==========================================
# 3. BASIC DATA PREPARATION
# ==========================================

df["Year"] = pd.to_numeric(
    df["Year"],
    errors="coerce"
)

df["Value"] = pd.to_numeric(
    df["Value"],
    errors="coerce"
)

print("\nEDA environment ready!")

# ==========================================
# 4. GLOBAL GDP TREND (2000-2024)
# ==========================================

print("\nAnalysing global GDP trends...")

gdp_df = df[
    df["Indicator_Category"] == "GDP_Current_USD"
].copy()

# Remove missing GDP observations
gdp_df = gdp_df.dropna(subset=["Value"])

# Aggregate GDP by year
global_gdp = (
    gdp_df.groupby("Year")["Value"]
    .sum()
    .reset_index()
)

# Convert USD to trillion USD
global_gdp["GDP_Trillion_USD"] = (
    global_gdp["Value"] / 1_000_000_000_000
)

# Display results
print("\nGLOBAL GDP BY YEAR")

print(
    global_gdp[
        ["Year", "GDP_Trillion_USD"]
    ].round(2).to_string(index=False)
)

# ==========================================
# 5. CREATE GDP TREND CHART
# ==========================================

plt.figure(figsize=(13, 6))

sns.lineplot(
    data=global_gdp,
    x="Year",
    y="GDP_Trillion_USD",
    marker="o",
    linewidth=2.5
)

plt.title(
    "Global GDP Trend (2000–2024)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Year", fontsize=12)

plt.ylabel("GDP (Trillion USD)", fontsize=12)

plt.xticks(
    range(2000, 2025, 2),
    rotation=45
)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "global_gdp_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nGlobal GDP chart saved successfully!")

# ==========================================
# 6. GDP GROWTH ANALYSIS
# ==========================================

print("\nAnalysing GDP growth...")

growth_df = df[
    df["Indicator_Category"] == "GDP_Growth"
].copy()

growth_df = growth_df.dropna(subset=["Value"])

# Calculate average growth across available economies
annual_growth = (
    growth_df.groupby("Year")["Value"]
    .mean()
    .reset_index()
)

annual_growth.rename(
    columns={"Value": "Average_GDP_Growth"},
    inplace=True
)

print("\nAVERAGE GDP GROWTH BY YEAR")

print(
    annual_growth.round(2).to_string(index=False)
)

# ==========================================
# 7. GDP GROWTH VISUALIZATION
# ==========================================

plt.figure(figsize=(13, 6))

sns.lineplot(
    data=annual_growth,
    x="Year",
    y="Average_GDP_Growth",
    marker="o",
    linewidth=2.5
)

plt.axhline(
    y=0,
    linestyle="--",
    alpha=0.7
)

plt.title(
    "Average GDP Growth Across Economies (2000–2024)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Year", fontsize=12)

plt.ylabel("Average GDP Growth (%)", fontsize=12)

plt.xticks(
    range(2000, 2025, 2),
    rotation=45
)

plt.grid(
    True,
    linestyle="--",
    alpha=0.4
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "average_gdp_growth.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nGDP growth chart saved successfully!")

# ==========================================
# 8. GDP PER CAPITA ANALYSIS
# ==========================================

print("\nAnalysing GDP per capita...")

gdp_pc = df[
    df["Indicator_Category"] == "GDP_Per_Capita"
].copy()

gdp_pc = gdp_pc.dropna(subset=["Value"])

# Latest available year for each country
latest_gdp_pc = (
    gdp_pc.sort_values("Year")
    .groupby("Country_Code")
    .tail(1)
)

# Top 10 countries
top_10 = latest_gdp_pc.nlargest(10, "Value")

print("\nTOP 10 COUNTRIES BY GDP PER CAPITA")

print(
    top_10[
        ["Country_Name", "Year", "Value"]
    ].round(2).to_string(index=False)
)

# ==========================================
# 9. GDP PER CAPITA CHART
# ==========================================

plt.figure(figsize=(13, 7))

sns.barplot(
    data=top_10.sort_values("Value", ascending=False),
    x="Value",
    y="Country_Name"
)

plt.title(
    "Top 10 Countries by GDP Per Capita",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("GDP Per Capita (Current US$)")

plt.ylabel("Country")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_10_gdp_per_capita.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nGDP per capita analysis completed!")
print("\nGDP PER CAPITA OBSERVATION YEARS")

print(
    top_10[
        ["Country_Name", "Year", "Value"]
    ].to_string(index=False)
)
# ==========================================
# 10. POPULATION ANALYSIS
# ==========================================

print("\nAnalysing population trends...")

population_df = df[
    df["Indicator_Category"] == "Population"
].copy()

population_df = population_df.dropna(subset=["Value"])

# Aggregate population by year
global_population = (
    population_df.groupby("Year")["Value"]
    .sum()
    .reset_index()
)

global_population["Population_Billions"] = (
    global_population["Value"] / 1_000_000_000
)

print("\nGLOBAL POPULATION BY YEAR")

print(
    global_population[
        ["Year", "Population_Billions"]
    ].round(2).to_string(index=False)
)

# ==========================================
# 11. GLOBAL POPULATION TREND CHART
# ==========================================

plt.figure(figsize=(13, 6))

sns.lineplot(
    data=global_population,
    x="Year",
    y="Population_Billions",
    marker="o",
    linewidth=2.5
)

plt.title(
    "Population Trend Across Economies (2000–2024)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Year")

plt.ylabel("Population (Billions)")

plt.xticks(range(2000, 2025, 2), rotation=45)

plt.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "global_population_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================
# 12. TOP 10 POPULATED ECONOMIES - 2024
# ==========================================

population_2024 = population_df[
    population_df["Year"] == 2024
].copy()

top_population = population_2024.nlargest(10, "Value")

print("\nTOP 10 POPULATED ECONOMIES - 2024")

print(
    top_population[
        ["Country_Name", "Value"]
    ].to_string(index=False)
)

# ==========================================
# 13. TOP 10 POPULATION CHART
# ==========================================

plt.figure(figsize=(13, 7))

sns.barplot(
    data=top_population.sort_values("Value", ascending=False),
    x="Value",
    y="Country_Name"
)

plt.title(
    "Top 10 Most Populated Economies (2024)",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Population")

plt.ylabel("Economy")

plt.tight_layout()

plt.savefig(
    CHART_DIR / "top_10_population_2024.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nPopulation analysis completed successfully!")