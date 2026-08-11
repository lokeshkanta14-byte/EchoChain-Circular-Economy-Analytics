from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("Electronics Products Silver Layer") \
    .getOrCreate()

# Input CSV
input_file = "electronics_products_pricing.csv"

# Read CSV
df = spark.read.csv(
    input_file,
    header=True,
    inferSchema=True
)

# Column names
print("\n========== COLUMN NAMES ==========")
for column in df.columns:
    print(column)

# Total records
print("\n========== TOTAL RECORDS ==========")
print(df.count())

# Schema
print("\n========== SCHEMA ==========")
df.printSchema()

# Show only selected useful columns
print("\n========== SAMPLE DATA ==========")

df.select(
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "weight"
).show(5, truncate=30)

# Stop Spark
spark.stop()