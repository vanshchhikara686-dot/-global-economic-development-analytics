
import pandas as pd
from pathlib import Path

# ==========================================
# 1. LOAD DATASET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "raw"
    / "worldbank_global_data_2000_2024.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "outputs"
    / "worldbank_validation_report.txt"
)

df = pd.read_csv(INPUT_FILE)

print("\nWORLD BANK DATA VALIDATION")
print("=" * 50)

# ==========================================
# 2. CHECK YEAR RANGE
# ==========================================

print("\n1. YEAR VALIDATION")

print("Minimum year:", df["Year"].min())
print("Maximum year:", df["Year"].max())

unexpected_years = df[
    ~df["Year"].between(2000, 2024)
]

print("Unexpected year records:", len(unexpected_years))

# ==========================================
# 3. CHECK INDICATOR COVERAGE
# ==========================================

print("\n2. INDICATOR VALIDATION")

expected_indicators = 10

actual_indicators = df["Indicator_Code"].nunique()

print("Expected indicators:", expected_indicators)
print("Actual indicators:", actual_indicators)

print("\nIndicator codes:")

print(
    df.groupby("Indicator_Category")["Indicator_Code"]
    .nunique()
)

# ==========================================
# 4. CHECK COUNTRY COVERAGE
# ==========================================

print("\n3. COUNTRY VALIDATION")

print("Unique countries:", df["Country_Code"].nunique())

print(
    "Unique country names:",
    df["Country_Name"].nunique()
)

# ==========================================
# 5. CHECK COUNTRY-YEAR COVERAGE
# ==========================================

print("\n4. COUNTRY-YEAR VALIDATION")

country_years = (
    df[["Country_Code", "Year"]]
    .drop_duplicates()
)

print("Unique country-year combinations:", len(country_years))

expected_combinations = (
    df["Country_Code"].nunique() * 25
)

print("Expected combinations if complete:", expected_combinations)

print(
    "Missing country-year combinations:",
    expected_combinations - len(country_years)
)

# ==========================================
# 6. CHECK DUPLICATES
# ==========================================

print("\n5. DUPLICATE VALIDATION")

duplicate_count = df.duplicated(
    subset=[
        "Country_Code",
        "Year",
        "Indicator_Code"
    ]
).sum()

print("Duplicate records:", duplicate_count)

# ==========================================
# 7. CHECK NEGATIVE VALUES
# ==========================================

print("\n6. NEGATIVE VALUE CHECK")

negative_values = (
    df[
        (df["Value"] < 0)
        & (df["Indicator_Category"] != "GDP_Growth")
    ]
)

print(
    "Negative values outside GDP growth:",
    len(negative_values)
)

if not negative_values.empty:
    print("\nNegative value examples:")
    print(
        negative_values[
            ["Country_Name", "Year",
             "Indicator_Category", "Value"]
        ].head(10)
    )

# ==========================================
# 8. CHECK VALUE DISTRIBUTION
# ==========================================

print("\n7. INDICATOR VALUE SUMMARY")

summary = (
    df.groupby("Indicator_Category")["Value"]
    .agg(["count", "min", "max", "mean"])
    .round(2)
)

print(summary)

# ==========================================
# 9. SAVE VALIDATION REPORT
# ==========================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

    file.write("WORLD BANK DATA VALIDATION REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write(f"Total records: {len(df):,}\n")
    file.write(f"Unique countries: {df['Country_Code'].nunique()}\n")
    file.write(f"Unique indicators: {actual_indicators}\n")
    file.write(f"Year range: {df['Year'].min()}-{df['Year'].max()}\n")
    file.write(f"Duplicate records: {duplicate_count}\n")
    file.write(f"Unexpected year records: {len(unexpected_years)}\n")
    file.write(
        f"Negative values outside GDP growth: {len(negative_values)}\n\n"
    )

    file.write("INDICATOR SUMMARY\n")
    file.write(summary.to_string())

print("\nValidation report saved:")
print(OUTPUT_FILE)

print("\nVALIDATION COMPLETED SUCCESSFULLY.")

