
import pandas as pd
from pathlib import Path

# Dataset folder
dataset_folder = Path("dataset/sales.csv")

# Find CSV or Excel files inside the dataset folder
files = (
    list(dataset_folder.rglob("*.csv"))
    + list(dataset_folder.rglob("*.xlsx"))
    + list(dataset_folder.rglob("*.xls"))
)

if not files:
    raise FileNotFoundError(
        "No CSV or Excel dataset found inside dataset/sales.csv"
    )

input_file = files[0]
print("Reading file:", input_file)

# Read the dataset based on file extension
if input_file.suffix.lower() == ".csv":
    df = pd.read_csv(input_file)
else:
    df = pd.read_excel(input_file)

print("Original shape:", df.shape)
print("Columns:", df.columns.tolist())

# Clean column names
df.columns = df.columns.astype(str).str.strip()

# Remove duplicate rows
df = df.drop_duplicates()

# Remove completely empty rows and columns
df = df.dropna(how="all")
df = df.dropna(axis=1, how="all")

# Remove extra spaces from text values
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].apply(
        lambda x: x.strip() if isinstance(x, str) else x
    )

# Save the cleaned dataset
output_file = Path("dataset/cleaned_global_superstore.csv")
df.to_csv(output_file, index=False)

print("\nCleaning completed successfully!")
print("Cleaned shape:", df.shape)
print("Saved to:", output_file)
print("\nMissing values:")
print(df.isnull().sum())
