
import pandas as pd
import os
import time

# =====================================
# CONFIGURATION
# =====================================

FILE_PATH = "data/raw/ecommerce_raw.csv"
CHUNK_SIZE = 100_000

# =====================================
# INITIALISE COUNTERS
# =====================================

total_rows = 0
total_missing = None
total_duplicates = 0

negative_quantities = 0
negative_prices = 0
negative_shipping = 0

start_time = time.time()

print("=" * 55)
print("FULL E-COMMERCE DATASET PROFILING")
print("=" * 55)

# =====================================
# PROCESS DATA IN CHUNKS
# =====================================

for chunk_number, chunk in enumerate(
    pd.read_csv(FILE_PATH, chunksize=CHUNK_SIZE),
    start=1
):

    total_rows += len(chunk)

    # Count missing values
    missing = chunk.isnull().sum()

    if total_missing is None:
        total_missing = missing
    else:
        total_missing += missing

    # Count completely duplicated rows within each chunk
    total_duplicates += chunk.duplicated().sum()

    # Identify invalid numerical values
    negative_quantities += (chunk["Quantity"] < 0).sum()
    negative_prices += (chunk["Unit_Price"] < 0).sum()
    negative_shipping += (chunk["Shipping_Cost"] < 0).sum()

    print(
        f"Processed {total_rows:,} records | "
        f"Chunk {chunk_number}"
    )

# =====================================
# FINAL REPORT
# =====================================

elapsed_time = time.time() - start_time

print("\n" + "=" * 55)
print("DATA QUALITY REPORT")
print("=" * 55)

print(f"\nTotal Records: {total_rows:,}")

print("\nMissing Values:")
print(total_missing)

print(f"\nDuplicate Records within chunks: {total_duplicates:,}")

print(f"\nNegative Quantities: {negative_quantities:,}")
print(f"Negative Prices: {negative_prices:,}")
print(f"Negative Shipping Costs: {negative_shipping:,}")

print(f"\nProcessing Time: {elapsed_time:.2f} seconds")

print("\nFull Dataset Profiling Completed!")

