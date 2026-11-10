import csv
import csv
import random
import os
from datetime import datetime, timedelta

# =====================================
# PROJECT CONFIGURATION
# =====================================

TOTAL_ROWS = 5_000_000
BATCH_SIZE = 100_000

OUTPUT_FILE = "data/raw/ecommerce_raw.csv"

random.seed(42)

# =====================================
# SAMPLE DATA
# =====================================

categories = [
    "Electronics", "Fashion", "Beauty",
    "Home & Kitchen", "Fitness", "Grocery"
]

products = {
    "Electronics": ["Laptop", "Smartphone", "Headphones", "Monitor"],
    "Fashion": ["T-Shirt", "Jeans", "Shoes", "Jacket"],
    "Beauty": ["Face Cream", "Shampoo", "Perfume", "Sunscreen"],
    "Home & Kitchen": ["Mixer", "Cookware", "Bedsheet", "Lamp"],
    "Fitness": ["Yoga Mat", "Dumbbells", "Treadmill", "Protein Shaker"],
    "Grocery": ["Rice", "Coffee", "Cooking Oil", "Snacks"]
}

payment_methods = [
    "UPI", "Credit Card", "Debit Card", "Cash on Delivery", "Net Banking"
]

order_statuses = [
    "Delivered", "Cancelled", "Returned", "Processing"
]

cities = [
    "Delhi", "Mumbai", "Bengaluru", "Hyderabad",
    "Chennai", "Pune", "Kolkata", "Jaipur",
    "Gurgaon", "Noida", "Lucknow", "Ahmedabad"
]

customer_segments = ["New", "Regular", "Loyal", "VIP"]

sales_channels = ["Website", "Mobile App", "Marketplace"]

# =====================================
# DATE CONFIGURATION
# =====================================

start_date = datetime(2021, 1, 1)
end_date = datetime(2025, 12, 31)

date_range_days = (end_date - start_date).days

# =====================================
# CREATE OUTPUT DIRECTORY
# =====================================

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# =====================================
# DATA GENERATION
# =====================================

columns = [
    "Order_ID",
    "Customer_ID",
    "Order_Date",
    "Product_ID",
    "Category",
    "Product_Name",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Payment_Method",
    "Order_Status",
    "City",
    "Customer_Segment",
    "Sales_Channel",
    "Shipping_Cost",
    "Total_Amount"
]

print("Starting dataset generation...")

with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow(columns)

    for batch_start in range(0, TOTAL_ROWS, BATCH_SIZE):

        batch = []

        current_batch_size = min(
            BATCH_SIZE,
            TOTAL_ROWS - batch_start
        )

        for i in range(current_batch_size):

            category = random.choice(categories)
            product = random.choice(products[category])

            quantity = random.randint(1, 10)
            unit_price = round(random.uniform(100, 50000), 2)
            discount = random.choice([0, 5, 10, 15, 20, 25])

            shipping_cost = round(random.uniform(30, 500), 2)

            total_amount = round(
                quantity * unit_price * (1 - discount / 100)
                + shipping_cost,
                2
            )

            order_date = start_date + timedelta(
                days=random.randint(0, date_range_days)
            )

            # Intentionally introduce data-quality problems
            customer_id = f"CUST{random.randint(10000, 99999)}"
            product_id = f"PROD{random.randint(1000, 9999)}"

            payment_method = random.choice(payment_methods)
            order_status = random.choice(order_statuses)
            city = random.choice(cities)
            segment = random.choice(customer_segments)
            channel = random.choice(sales_channels)

            # Missing values
            if random.random() < 0.02:
                customer_id = ""

            if random.random() < 0.01:
                product = ""

            if random.random() < 0.01:
                city = ""

            # Inconsistent category formatting
            if random.random() < 0.01:
                category = category.upper()

            if random.random() < 0.005:
                category = f" {category} "

            # Invalid numerical values
            if random.random() < 0.001:
                quantity = -quantity

            if random.random() < 0.001:
                unit_price = -unit_price

            # Duplicate records
            if random.random() < 0.005 and batch:
                row = random.choice(batch)
            else:
                row = [
                    f"ORD{batch_start + i + 1:08d}",
                    customer_id,
                    order_date.strftime("%Y-%m-%d"),
                    product_id,
                    category,
                    product,
                    quantity,
                    unit_price,
                    discount,
                    payment_method,
                    order_status,
                    city,
                    segment,
                    channel,
                    shipping_cost,
                    total_amount
                ]

            batch.append(row)

        writer.writerows(batch)

        completed = batch_start + current_batch_size

        print(
            f"Generated {completed:,} / {TOTAL_ROWS:,} records "
            f"({completed / TOTAL_ROWS * 100:.1f}%)"
        )

print("\nDataset generation completed!")
print(f"Saved to: {OUTPUT_FILE}")

