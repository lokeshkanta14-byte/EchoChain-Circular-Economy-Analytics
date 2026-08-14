import pandas as pd

file_path = "data/raw/electronics_products_pricing.csv"

df = pd.read_csv(file_path)

print("===== DATASET VALIDATION =====")

print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nData types:")
print(df.dtypes)

print("\nFirst 5 rows:")
print(df.head())

print("\n===== VALIDATION COMPLETED =====")