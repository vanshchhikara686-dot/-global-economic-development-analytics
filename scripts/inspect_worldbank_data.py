
import pandas as pd
from pathlib import Path

# ==========================================
# 1. LOAD DATASET
# ==========================================

DATA_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "worldbank_global_data_2000_2024.csv"
)

df = pd.read_csv(DATA_FILE)

# ==========================================
# 2. BASIC DATASET INFORMATION
# ==========================================

print("\n========== DATASET OVERVIEW ==========")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())

# ==========================================
# 3. DATA TYPES
# ==========================================

print("\n========== DATA TYPES ==========")

print(df.dtypes)

# ==========================================
# 4. MISSING VALUES
# ==========================================

print("\n========== MISSING VALUES ==========")

missing = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": (
        df.isnull().mean() * 100
    ).round(2)
})

print(missing)

# ==========================================
# 5. COUNTRY AND INDICATOR COUNTS
# ==========================================

print("\n========== COUNTRY INFORMATION ==========")

print("Unique Countries:", df["Country_Code"].nunique())

print("\n========== INDICATOR COUNTS ==========")

print(
    df.groupby("Indicator_Category").size()
)

# ==========================================
# 6. YEAR RANGE
# ==========================================

print("\n========== YEAR INFORMATION ==========")

print("Minimum Year:", df["Year"].min())
print("Maximum Year:", df["Year"].max())

# ==========================================
# 7. DUPLICATE CHECK
# ==========================================

print("\n========== DUPLICATE CHECK ==========")

print("Duplicate Rows:", df.duplicated().sum())

# ==========================================
# 8. DATA PREVIEW
# ==========================================

print("\n========== FIRST 10 ROWS ==========")

print(df.head(10).to_string(index=False))

# ==========================================
# 9. DATA VALIDATION COMPLETE
# ==========================================

print("\nDATASET INSPECTION COMPLETED SUCCESSFULLY.")

