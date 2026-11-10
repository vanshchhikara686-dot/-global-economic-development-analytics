import pandas as pd
import numpy as np
import os
import time
# ==========================================
# STAGE 2 - STEP 1: TEXT STANDARDISATION
# ==========================================

def standardise_text(df):

    print("\nSTANDARDISING TEXT COLUMNS")

    text_columns = [
        "Category",
        "Product_Name",
        "City",
        "Customer_Segment",
        "Sales_Channel",
        "Order_Status",
        "Payment_Method"
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    title_columns = [
        "Category",
        "Product_Name",
        "City",
        "Customer_Segment",
        "Sales_Channel",
        "Order_Status"
    ]

    for column in title_columns:
        if column in df.columns:
            df[column] = df[column].str.title()

    if "Payment_Method" in df.columns:
        df["Payment_Method"] = df["Payment_Method"].str.upper()

    print("Text standardisation completed!")

    return df
# ==========================================
# STAGE 2 - STEP 2: DATA TYPE CORRECTION
# ==========================================

def correct_data_types(df):

    print("\nCORRECTING DATA TYPES")

    # Convert ID columns to string
    id_columns = [
        "Order_ID",
        "Customer_ID",
        "Product_ID"
    ]

    for column in id_columns:
        if column in df.columns:
            df[column] = df[column].astype("string")

    # Convert Order_Date to datetime
    if "Order_Date" in df.columns:
        df["Order_Date"] = pd.to_datetime(
            df["Order_Date"],
            errors="coerce"
        )

    # Convert numerical columns
    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Discount",
        "Shipping_Cost",
        "Total_Amount"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Convert Quantity to nullable integer
    if "Quantity" in df.columns:
        df["Quantity"] = df["Quantity"].astype("Int64")

    print("\nUpdated Data Types:")
    print(df.dtypes)

    print("\nData type correction completed!")

    return df
# ==========================================
# E-COMMERCE DATA CLEANING PIPELINE V2
# ==========================================
# ==========================================
# STAGE 2 - STEP 3: NUMERICAL VALIDATION
# ==========================================

def validate_numeric_values(df):

    print("\nNUMERICAL DATA VALIDATION")

    # Check negative quantities
    negative_quantity = (df["Quantity"] < 0).sum()

    # Check negative unit prices
    negative_prices = (df["Unit_Price"] < 0).sum()

    # Check invalid discounts
    invalid_discount = (
        (df["Discount"] < 0) |
        (df["Discount"] > 100)
    ).sum()

    # Check negative shipping costs
    negative_shipping = (
        df["Shipping_Cost"] < 0
    ).sum()

    print("\nNUMERICAL VALIDATION RESULTS")

    print("Negative Quantities:", negative_quantity)
    print("Negative Unit Prices:", negative_prices)
    print("Invalid Discounts:", invalid_discount)
    print("Negative Shipping Costs:", negative_shipping)

    print("\nNumerical validation completed!")

    return df
# ==========================================
# STAGE 2 - STEP 4: REMOVE INVALID RECORDS
# ==========================================

def remove_invalid_records(df):

    print("\nREMOVING INVALID RECORDS")

    rows_before = len(df)

    invalid_mask = (
        (df["Quantity"] <= 0) |
        (df["Unit_Price"] < 0) |
        (df["Discount"] < 0) |
        (df["Discount"] > 100) |
        (df["Shipping_Cost"] < 0)
    )

    invalid_count = invalid_mask.sum()

    df = df.loc[~invalid_mask].copy()

    rows_after = len(df)

    print("Invalid records removed:", invalid_count)
    print("Records before:", rows_before)
    print("Records after:", rows_after)

    print("\nInvalid record removal completed!")

    return df
# ==========================================
# STAGE 2 - STEP 5: BUSINESS RULE VALIDATION
# ==========================================

def validate_business_rules(df):

    print("\nBUSINESS RULE VALIDATION")

    # Calculate expected transaction amount
    expected_amount = (
        df["Quantity"] *
        df["Unit_Price"] *
        (1 - df["Discount"] / 100) +
        df["Shipping_Cost"]
    )

    # Compare expected and existing amounts
    difference = (
        df["Total_Amount"] - expected_amount
    ).abs()

    # Allow a small rounding difference
    mismatch_count = (difference > 0.01).sum()

    print("\nBUSINESS RULE RESULTS")

    print("Total records checked:", len(df))
    print("Incorrect transaction totals:", mismatch_count)

    print("\nBusiness rule validation completed!")

    return df
# ==========================================
# STAGE 2 - STEP 6: OUTLIER DETECTION
# ==========================================

def detect_outliers(df):

    print("\nOUTLIER DETECTION USING IQR")

    columns = [
        "Quantity",
        "Unit_Price",
        "Shipping_Cost",
        "Total_Amount"
    ]

    for column in columns:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - (1.5 * IQR)
        upper_bound = Q3 + (1.5 * IQR)

        outlier_count = (
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ).sum()

        print(f"\nColumn: {column}")
        print("Q1:", round(Q1, 2))
        print("Q3:", round(Q3, 2))
        print("IQR:", round(IQR, 2))
        print("Lower Bound:", round(lower_bound, 2))
        print("Upper Bound:", round(upper_bound, 2))
        print("Outliers Found:", outlier_count)

    print("\nOutlier detection completed!")

    return df
# ==========================================
# STAGE 2 - STEP 7: MEMORY OPTIMISATION
# ==========================================

def optimize_memory(df):

    print("\nMEMORY OPTIMISATION")

    # Measure memory before optimisation
    memory_before = (
        df.memory_usage(deep=True).sum() / 1024**2
    )

    print("Memory before:", round(memory_before, 2), "MB")

    # Convert repetitive text columns to category
    categorical_columns = [
        "Category",
        "Payment_Method",
        "Order_Status",
        "City",
        "Customer_Segment",
        "Sales_Channel"
    ]

    for column in categorical_columns:
        if column in df.columns:
            df[column] = df[column].astype("category")

    # Downcast numerical columns
    integer_columns = [
        "Quantity",
        "Discount"
    ]

    for column in integer_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                downcast="integer"
            )

    float_columns = [
        "Unit_Price",
        "Shipping_Cost",
        "Total_Amount"
    ]

    for column in float_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                downcast="float"
            )

    # Measure memory after optimisation
    memory_after = (
        df.memory_usage(deep=True).sum() / 1024**2
    )

    reduction = (
        (memory_before - memory_after) / memory_before
    ) * 100

    print("Memory after:", round(memory_after, 2), "MB")
    print("Memory reduction:", round(reduction, 2), "%")

    print("\nMemory optimisation completed!")

    return df
START_TIME = time.time()

INPUT_FILE = "data/raw/ecommerce_raw.csv"
OUTPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"
REPORT_FILE = "outputs/data_quality_report.txt"

print("=" * 60)
print("E-COMMERCE DATA CLEANING PIPELINE")
print("=" * 60)

# Create output directories if they don't exist
os.makedirs("data/cleaned", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

print("\nProject setup completed.")
# ==========================================
# STEP 1: LOAD AND INSPECT DATASET
# ==========================================

print("\nSTEP 1: LOADING DATASET")

try:
    # Load dataset
    df = pd.read_csv(INPUT_FILE)
    print("\nDataset loaded successfully!")

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Records:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Records:")
    print(df.duplicated().sum())
    # STEP 2: REMOVE DUPLICATES

    print("\nSTEP 2: REMOVING DUPLICATES")

    rows_before = len(df)

    df = df.drop_duplicates()

    rows_after = len(df)

    print(f"Duplicates removed: {rows_before - rows_after}")
    print(f"Records remaining: {rows_after}")


    # STEP 3: HANDLE MISSING VALUES

    print("\nSTEP 3: HANDLING MISSING VALUES")

    missing_before = df.isnull().sum().sum()

        # Handle missing categorical values

    if "Product_Name" in df.columns:
        df["Product_Name"] = df["Product_Name"].fillna("Unknown")

    if "Customer_ID" in df.columns:
        df["Customer_ID"] = df["Customer_ID"].fillna("Unknown")

    if "City" in df.columns:
        df["City"] = df["City"].fillna("Unknown")

    missing_after = df.isnull().sum().sum()

    print(f"Missing values before: {missing_before}")
    print(f"Missing values after: {missing_after}")
    # STAGE 2 - STEP 1: STANDARDISE TEXT
    df = standardise_text(df)
    # STAGE 2 - STEP 2: DATA TYPE CORRECTION
    df = correct_data_types(df)
    # STAGE 2 - STEP 3: NUMERICAL VALIDATION
    df = validate_numeric_values(df)
     # STAGE 2 - STEP 4: REMOVE INVALID RECORDS
    df = remove_invalid_records(df)
    # STAGE 2 - STEP 5: BUSINESS RULE VALIDATION
    df = validate_business_rules(df)
    # STAGE 2 - STEP 6: OUTLIER DETECTION
    df = detect_outliers(df)
    # STAGE 2 - STEP 7: MEMORY OPTIMISATION
    df = optimize_memory(df)
    # STEP 4: SAVE CLEANED DATASET

    print("\nSTEP 4: SAVING CLEANED DATASET")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Cleaned dataset saved to: {OUTPUT_FILE}")
    print(f"Final dataset shape: {df.shape}")
except FileNotFoundError:
    print(f"\nERROR: Dataset not found at {INPUT_FILE}")

except Exception as e:
    print(f"\nERROR: {e}")