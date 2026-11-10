
import pandas as pd
from pathlib import Path

# ==========================================
# 1. LOAD RAW DATA
# ==========================================

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "worldbank_global_data_2000_2024.csv"
)

df = pd.read_csv(DATA_FILE)

# ==========================================
# 2. INDICATOR QUALITY ANALYSIS
# ==========================================

quality = (
    df.groupby("Indicator_Category")
    .agg(
        Total_Records=("Value", "size"),
        Available_Values=("Value", "count"),
        Missing_Values=("Value", lambda x: x.isna().sum()),
        Unique_Countries=("Country_Code", "nunique"),
        First_Year=("Year", "min"),
        Last_Year=("Year", "max")
    )
    .reset_index()
)

quality["Available_Percentage"] = (
    quality["Available_Values"]
    / quality["Total_Records"]
    * 100
).round(2)

quality["Missing_Percentage"] = (
    quality["Missing_Values"]
    / quality["Total_Records"]
    * 100
).round(2)

# ==========================================
# 3. DISPLAY RESULTS
# ==========================================

print("\n========== INDICATOR QUALITY REPORT ==========\n")

print(
    quality.to_string(index=False)
)

# ==========================================
# 4. DUPLICATE CHECK
# ==========================================

print("\n========== DUPLICATE ANALYSIS ==========\n")

duplicates = df.duplicated(
    subset=[
        "Country_Code",
        "Year",
        "Indicator_Code"
    ]
).sum()

print("Duplicate country-year-indicator records:", duplicates)

# ==========================================
# 5. SAVE QUALITY REPORT
# ==========================================

OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "outputs"
    / "indicator_quality_report.csv"
)

quality.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\nQuality report saved successfully:")
print(OUTPUT_FILE)

