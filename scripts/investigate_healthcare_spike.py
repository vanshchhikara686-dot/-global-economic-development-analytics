import pandas as pd
from pathlib import Path

# ==========================================
# 1. FILE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "cleaned"
    / "worldbank_global_cleaned.csv"
)

OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# ==========================================
# 2. LOAD DATA
# ==========================================

df = pd.read_csv(INPUT_FILE)

health = df[
    df["Indicator_Category"] == "Health_Expenditure"
].copy()

health["Value"] = pd.to_numeric(
    health["Value"],
    errors="coerce"
)

health = health.dropna(subset=["Value"])

print("\nHEALTHCARE EXPENDITURE DATA")
print("=" * 50)

print("Total records:", len(health))
print("Unique countries:", health["Country_Code"].nunique())

# ==========================================
# 3. YEARLY STATISTICS
# ==========================================

yearly = (
    health.groupby("Year")
    .agg(
        Reporting_Countries=("Country_Code", "nunique"),
        Average_Expenditure=("Value", "mean"),
        Median_Expenditure=("Value", "median"),
        Minimum=("Value", "min"),
        Maximum=("Value", "max")
    )
    .reset_index()
)

print("\nYEARLY HEALTHCARE EXPENDITURE STATISTICS")
print("=" * 80)

print(yearly.round(2).to_string(index=False))

yearly.to_csv(
    OUTPUT_DIR / "healthcare_yearly_diagnostic.csv",
    index=False
)

# ==========================================
# 4. COMPARE 2023 AND 2024
# ==========================================

print("\n2023 VS 2024 COMPARISON")
print("=" * 50)

comparison = yearly[
    yearly["Year"].isin([2023, 2024])
]

print(comparison.round(2).to_string(index=False))

# ==========================================
# 5. TOP 15 COUNTRIES IN 2024
# ==========================================

latest = health[health["Year"] == 2024]

top_15 = latest.sort_values(
    "Value",
    ascending=False
).head(15)

print("\nTOP 15 COUNTRIES BY HEALTHCARE EXPENDITURE (2024)")
print("=" * 75)

print(
    top_15[
        ["Country_Name", "Value"]
    ].to_string(index=False)
)

top_15.to_csv(
    OUTPUT_DIR / "healthcare_top15_2024.csv",
    index=False
)

# ==========================================
# 6. FINAL SUMMARY
# ==========================================

print("\nDIAGNOSTIC FILES SAVED SUCCESSFULLY")
print("1. healthcare_yearly_diagnostic.csv")
print("2. healthcare_top15_2024.csv")
# ==========================================
# 7. COMPARABLE COUNTRY ANALYSIS
# ==========================================

print("\nCOMPARABLE COUNTRY ANALYSIS")
print("=" * 60)

# Identify countries reporting in 2024
countries_2024 = set(
    health.loc[
        health["Year"] == 2024,
        "Country_Code"
    ]
)

# Filter historical data to those same countries
comparable = health[
    health["Country_Code"].isin(countries_2024)
].copy()

# Calculate yearly statistics for the same countries
comparable_yearly = (
    comparable.groupby("Year")
    .agg(
        Reporting_Countries=("Country_Code", "nunique"),
        Average_Expenditure=("Value", "mean"),
        Median_Expenditure=("Value", "median")
    )
    .reset_index()
)

print("\nSAME-COUNTRY HEALTHCARE EXPENDITURE TREND")

print(
    comparable_yearly.round(2).to_string(index=False)
)

comparable_yearly.to_csv(
    OUTPUT_DIR / "healthcare_comparable_countries.csv",
    index=False
)

print("\nComparable-country analysis saved successfully!")