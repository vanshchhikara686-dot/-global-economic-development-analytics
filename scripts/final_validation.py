import pandas as pd
import os

# File location
INPUT_FILE = "data/cleaned/ecommerce_cleaned.csv"

print("=" * 60)
print("FINAL DATA QUALITY VALIDATION")
print("=" * 60)

# Load cleaned dataset
df = pd.read_csv(INPUT_FILE)

print("\n1. DATASET OVERVIEW")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Check missing values
print("\n2. MISSING VALUES")
print(df.isnull().sum())
print("Total missing values:", df.isnull().sum().sum())

# Check duplicate records
print("\n3. DUPLICATE RECORDS")
print("Duplicate rows:", df.duplicated().sum())

# Check invalid numerical values
print("\n4. NUMERICAL VALIDATION")

print("Negative quantities:", (df["Quantity"] < 0).sum())
print("Negative unit prices:", (df["Unit_Price"] < 0).sum())
print("Invalid discounts:", ((df["Discount"] < 0) | (df["Discount"] > 100)).sum())
print("Negative shipping costs:", (df["Shipping_Cost"] < 0).sum())

# Check date range
print("\n5. DATE VALIDATION")
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

print("Invalid dates:", df["Order_Date"].isnull().sum())
print("Earliest order:", df["Order_Date"].min())
print("Latest order:", df["Order_Date"].max())

# Count unique entities
print("\n6. UNIQUE RECORDS")
print("Unique customers:", df["Customer_ID"].nunique())
print("Unique products:", df["Product_ID"].nunique())
print("Unique orders:", df["Order_ID"].nunique())

print("\n" + "=" * 60)
print("FINAL VALIDATION COMPLETED")
print("=" * 60)