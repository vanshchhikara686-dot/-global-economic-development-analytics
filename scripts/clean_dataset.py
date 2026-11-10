import pandas as pd
import numpy as np
import os
import time

# =====================================
# CONFIGURATION
# =====================================

INPUT_FILE = "data/raw/ecommerce_raw.csv"

OUTPUT_FILE = "data/processed/ecommerce_cleaned.csv"

CHUNK_SIZE = 100_000

os.makedirs("data/processed", exist_ok=True)

print("E-commerce Data Cleaning Pipeline")
print("=" * 50)

# =====================================
# HANDLE MISSING VALUES
# =====================================

def handle_missing_values(df):

    missing_before = df.isnull().sum().sum()

    # Replace missing categorical values
    columns_to_fill = [
        "Customer_ID",
        "Product_Name",
        "City"
    ]

    for column in columns_to_fill:
        df[column] = df[column].fillna("UNKNOWN")

    missing_after = df.isnull().sum().sum()

    print("\nMissing Value Report")
    print("-" * 40)

    print(f"Missing values before cleaning: {missing_before:,}")
    print(f"Missing values after cleaning: {missing_after:,}")

    return df


# =====================================
# TEST ON 100,000 RECORDS
# =====================================

print("\nTesting missing-value cleaning...")

df = pd.read_csv(INPUT_FILE, nrows=100_000)

print("\nBefore Cleaning:")
print(df.isnull().sum())

df = handle_missing_values(df)

print("\nAfter Cleaning:")
print(df.isnull().sum())

print("\nTest completed successfully!")


# =====================================
# REMOVE DUPLICATE RECORDS
# =====================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    removed = before - after

    print("\nDuplicate Removal Report")
    print("-" * 40)

    print(f"Records before: {before:,}")
    print(f"Records after: {after:,}")
    print(f"Duplicates removed: {removed:,}")

    return df

# =====================================
# INVESTIGATE INVALID NUMERICAL VALUES
# =====================================

def investigate_invalid_values(df):

    print("\nNUMERICAL DATA QUALITY INVESTIGATION")
    print("=" * 45)

    print("\nQuantity Analysis:")
    print("Negative quantities:", (df["Quantity"] < 0).sum())
    print("Zero quantities:", (df["Quantity"] == 0).sum())

    print("\nUnit Price Analysis:")
    print("Negative prices:", (df["Unit_Price"] < 0).sum())
    print("Zero prices:", (df["Unit_Price"] == 0).sum())

    print("\nShipping Cost Analysis:")
    print("Negative shipping:", (df["Shipping_Cost"] < 0).sum())

    print("\nQuantity Statistics:")
    print(df["Quantity"].describe())

    print("\nUnit Price Statistics:")
    print(df["Unit_Price"].describe())

    print("\nTotal Amount Statistics:")
    print(df["Total_Amount"].describe())

    return df

# =====================================
# INVESTIGATE INVALID NUMERICAL VALUES
# =====================================

def investigate_invalid_values(df):

    print("\nNUMERICAL DATA QUALITY INVESTIGATION")
    print("=" * 45)

    print("\nQuantity Analysis:")
    print("Negative quantities:", (df["Quantity"] < 0).sum())
    print("Zero quantities:", (df["Quantity"] == 0).sum())

    print("\nUnit Price Analysis:")
    print("Negative prices:", (df["Unit_Price"] < 0).sum())
    print("Zero prices:", (df["Unit_Price"] == 0).sum())

    print("\nShipping Cost Analysis:")
    print("Negative shipping:", (df["Shipping_Cost"] < 0).sum())

    print("\nQuantity Statistics:")
    print(df["Quantity"].describe())

    print("\nUnit Price Statistics:")
    print(df["Unit_Price"].describe())

    print("\nTotal Amount Statistics:")
    print(df["Total_Amount"].describe())


    print("\nNEGATIVE QUANTITY RECORDS:")
    print(
        df[df["Quantity"] < 0][
            ["Order_ID", "Product_Name", "Quantity",
             "Unit_Price", "Total_Amount", "Order_Status"]
        ].head(10)
    )

    print("\nNEGATIVE UNIT PRICE RECORDS:")
    print(
        df[df["Unit_Price"] < 0][
            ["Order_ID", "Product_Name", "Quantity",
             "Unit_Price", "Total_Amount", "Order_Status"]
        ].head(10)
    )

    return df
# =====================================
# TEST CLEANING ON 100,000 RECORDS
# =====================================

print("\nStarting cleaning test...")

df = pd.read_csv(INPUT_FILE, nrows=100_000)

print("\nOriginal Dataset:")
print(f"Total Records: {len(df):,}")

# Step 1: Handle missing values
df = handle_missing_values(df)

# Step 2: Remove duplicate records
df = remove_duplicates(df)
df = investigate_invalid_values(df)

# =====================================
# FINAL TEST REPORT
# =====================================

print("\nFinal Cleaning Report")
print("=" * 40)

print(f"Final Records: {len(df):,}")
print(f"Remaining Missing Values: {df.isnull().sum().sum():,}")
print(f"Remaining Duplicates: {df.duplicated().sum():,}")

print("\nCleaning Test Completed!")







