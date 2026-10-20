
import pandas as pd
from pathlib import Path

# Load cleaned dataset
input_file = Path("dataset/cleaned_global_superstore.csv")
df = pd.read_csv(input_file)

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Ensure numerical columns have numeric data types
for col in ["Sales", "Profit", "Quantity"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove rows missing essential analysis values
df = df.dropna(subset=["Order Date", "Sales", "Profit"])

# Create output folder
output_folder = Path("analysis/results")
output_folder.mkdir(parents=True, exist_ok=True)

# 1. Overall performance
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order ID"].nunique()

print("===== SALES PERFORMANCE =====")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Quantity Sold: {total_quantity:,}")
print(f"Total Orders: {total_orders:,}")

# 2. Sales by category
category_sales = (
    df.groupby("Category", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)
category_sales.to_csv(output_folder / "sales_by_category.csv", index=False)

print("\n===== SALES BY CATEGORY =====")
print(category_sales.to_string(index=False))

# 3. Sales by region
region_sales = (
    df.groupby("Region", as_index=False)["Sales"]
    .sum()
    .sort_values("Sales", ascending=False)
)
region_sales.to_csv(output_folder / "sales_by_region.csv", index=False)

print("\n===== SALES BY REGION =====")
print(region_sales.to_string(index=False))

# 4. Top 10 products by sales
top_products = (
    df.groupby("Product Name", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)
top_products.to_csv(output_folder / "top_10_products.csv", index=False)

print("\n===== TOP 10 PRODUCTS =====")
print(top_products.to_string(index=False))

# 5. Monthly sales trend
df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Year-Month", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Year-Month")
)
monthly_sales.to_csv(output_folder / "monthly_sales_trend.csv", index=False)

print("\n===== MONTHLY SALES TREND =====")
print(monthly_sales.to_string(index=False))

# 6. Profit by category
category_profit = (
    df.groupby("Category", as_index=False)["Profit"]
    .sum()
    .sort_values("Profit", ascending=False)
)
category_profit.to_csv(output_folder / "profit_by_category.csv", index=False)

print("\nAnalysis completed successfully!")
print("Result files saved in:", output_folder)
