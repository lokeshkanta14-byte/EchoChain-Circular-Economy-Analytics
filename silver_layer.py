from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim
from functools import reduce

# Create Spark Session
spark = SparkSession.builder \
    .appName("Electronics Products Silver Layer") \
    .getOrCreate()

# Input CSV
input_file = "electronics_products_pricing.csv"


# ============================================================
# 1. READ RAW DATA
# ============================================================

df = spark.read.csv(
    input_file,
    header=True,
    inferSchema=True
)

print("\n========== RAW DATA ==========")
print("Total records:", df.count())


# ============================================================
# 2. COLUMN NAMES
# ============================================================

print("\n========== COLUMN NAMES ==========")

for column in df.columns:
    print(column)


# ============================================================
# 3. REMOVE DUPLICATE RECORDS
# ============================================================

before_duplicates = df.count()

df = df.dropDuplicates()

after_duplicates = df.count()

print("\n========== DUPLICATE REMOVAL ==========")
print("Records before removing duplicates:", before_duplicates)
print("Records after removing duplicates:", after_duplicates)
print("Duplicates removed:", before_duplicates - after_duplicates)


# ============================================================
# 4. REMOVE COMPLETELY EMPTY RECORDS
# ============================================================

before_empty = df.count()

# Use backticks around column names because some columns
# contain dots such as prices.availability
non_null_conditions = [
    col(f"`{column}`").isNotNull()
    for column in df.columns
]

df = df.filter(
    reduce(lambda x, y: x | y, non_null_conditions)
)

after_empty = df.count()

print("\n========== EMPTY ROW REMOVAL ==========")
print("Records before removing empty rows:", before_empty)
print("Records after removing empty rows:", after_empty)
print("Empty rows removed:", before_empty - after_empty)


# ============================================================
# 5. REMOVE RECORDS WITH MISSING ID
# ============================================================

before_missing_id = df.count()

df = df.filter(
    col("id").isNotNull()
)

after_missing_id = df.count()

print("\n========== MISSING ID REMOVAL ==========")
print("Records before removing missing IDs:", before_missing_id)
print("Records after removing missing IDs:", after_missing_id)
print("Records removed:", before_missing_id - after_missing_id)


# ============================================================
# 6. HANDLE MISSING VALUES
# ============================================================

print("\n========== MISSING VALUE HANDLING ==========")

df = df.fillna({
    "name": "Unknown",
    "brand": "Unknown",
    "categories": "Unknown"
})

print("Missing values handled for name, brand and categories.")


# ============================================================
# 7. CLEAN TEXT COLUMNS
# ============================================================

print("\n========== TEXT CLEANING ==========")

df = df.withColumn(
    "name",
    trim(col("name"))
)

df = df.withColumn(
    "brand",
    trim(col("brand"))
)

df = df.withColumn(
    "categories",
    trim(col("categories"))
)

print("Trimmed extra spaces from name, brand and categories.")


# ============================================================
# 8. CONVERT PRICE TO NUMERIC TYPE
# ============================================================

print("\n========== PRICE TYPE CONVERSION ==========")

df = df.withColumn(
    "price",
    col("price").cast("double")
)

print("Price converted to numeric type.")


# ============================================================
# 9. FINAL RECORD COUNT
# ============================================================

print("\n========== CLEANED RECORD COUNT ==========")

print("Final records:", df.count())


# ============================================================
# 10. FINAL SCHEMA
# ============================================================

print("\n========== FINAL SCHEMA ==========")

df.printSchema()


# ============================================================
# 11. CLEANED SAMPLE DATA
# ============================================================

print("\n========== CLEANED SAMPLE DATA ==========")

df.select(
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "weight"
).show(5, truncate=30)


# ============================================================
# STOP SPARK
# ============================================================

spark.stop()