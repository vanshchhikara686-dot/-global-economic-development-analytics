
import pandas as pd
from pathlib import Path

# ==========================================
# 1. FILE PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "raw"
    / "worldbank_global_data_2000_2024.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "cleaned"
    / "worldbank_global_cleaned.csv"
)

# ==========================================
# 2. LOAD ORIGINAL DATA
# ==========================================

print("Loading World Bank dataset...")

df = pd.read_csv(INPUT_FILE)

original_rows = len(df)

print("Original records:", original_rows)

# ==========================================
# 3. DATA TYPE VALIDATION
# ==========================================

df["Country_Code"] = df["Country_Code"].astype("string")

df["Country_Name"] = df["Country_Name"].astype("string")

df["Indicator_Code"] = df["Indicator_Code"].astype("string")

df["Indicator_Name"] = df["Indicator_Name"].astype("string")

df["Indicator_Category"] = df["Indicator_Category"].astype("string")

df["Year"] = pd.to_numeric(
    df["Year"],
    errors="coerce"
).astype("Int64")

df["Value"] = pd.to_numeric(
    df["Value"],
    errors="coerce"
)

# ==========================================
# 4. CHECK MISSING IDENTIFIERS
# ==========================================

identifier_columns = [
    "Country_Code",
    "Country_Name",
    "Year",
    "Indicator_Code",
    "Indicator_Category"
]

missing_identifiers = df[identifier_columns].isna().any(axis=1)

print(
    "Rows with missing identifiers:",
    missing_identifiers.sum()
)

# Remove only records with missing identifiers
df = df.loc[~missing_identifiers].copy()

# ==========================================
# 5. CHECK YEAR RANGE
# ==========================================

df = df[
    df["Year"].between(2000, 2024)
].copy()

# ==========================================
# 6. CHECK DUPLICATES
# ==========================================

duplicate_count = df.duplicated(
    subset=[
        "Country_Code",
        "Year",
        "Indicator_Code"
    ]
).sum()

print("Duplicate records detected:", duplicate_count)

# Remove duplicate country-year-indicator records
df = df.drop_duplicates(
    subset=[
        "Country_Code",
        "Year",
        "Indicator_Code"
    ]
)

# ==========================================
# 7. PRESERVE MISSING INDICATOR VALUES
# ==========================================

missing_values = df["Value"].isna().sum()

print("Missing indicator values preserved:", missing_values)

# ==========================================
# 8. ADD DATA AVAILABILITY FLAG
# ==========================================

df["Data_Availability"] = df["Value"].notna().map({
    True: "Available",
    False: "Missing"
})

# ==========================================
# 9. SORT DATASET
# ==========================================

df = df.sort_values(
    by=[
        "Country_Name",
        "Year",
        "Indicator_Category"
    ]
).reset_index(drop=True)

# ==========================================
# 10. EXPORT CLEANED DATA
# ==========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

# ==========================================
# 11. CLEANING SUMMARY
# ==========================================

print("\n" + "=" * 50)

print("WORLD BANK DATA CLEANING COMPLETED")

print("=" * 50)

print("Original rows:", original_rows)

print("Final rows:", len(df))

print("Countries:", df["Country_Code"].nunique())

print("Indicators:", df["Indicator_Code"].nunique())

print("Missing values preserved:", missing_values)

print("Final columns:", len(df.columns))

print("\nCleaned dataset saved at:")

print(OUTPUT_FILE)

print("\nDATA CLEANING COMPLETED SUCCESSFULLY.")

