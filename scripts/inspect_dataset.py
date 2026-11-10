import pandas as pd
import os

# Dataset location
file_path = "data/raw/ecommerce_raw.csv"

# File size
file_size = os.path.getsize(file_path) / (1024 ** 3)

print("=" * 50)
print("ECOMMERCE DATASET INSPECTION")
print("=" * 50)

print(f"\nFile Size: {file_size:.2f} GB")

# Read only first 10,000 rows for safe inspection
df = pd.read_csv(file_path, nrows=10000)

print("\nFirst 5 Records:")
print(df.head())

print("\nDataset Shape (sample):")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records in Sample:")
print(df.duplicated().sum())

print("\nMemory Usage:")
print(f"{df.memory_usage(deep=True).sum() / (1024 ** 2):.2f} MB")

print("\nInspection Completed!")