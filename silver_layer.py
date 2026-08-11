from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when, regexp_extract
from functools import reduce

# ============================================================
# CREATE SPARK SESSION
# ============================================================

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

# Backticks are required for columns containing dots
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
# 8. SAFE PRICE TYPE CONVERSION
# ============================================================

print("\n========== PRICE TYPE CONVERSION ==========")

# Convert only values that contain a valid numeric price.
# Invalid text such as:
# "Warranty: 1 Year Manufacturer Warranty"
# will become NULL instead of causing a Spark error.

price_as_string = trim(col("price").cast("string"))

df = df.withColumn(
    "price",
    when(
        price_as_string.rlike(r"^-?\d+(\.\d+)?$"),
        price_as_string.cast("double")
    ).otherwise(None)
)

print("Price converted safely to numeric type.")
print("Invalid/non-numeric price values converted to NULL.")


# ============================================================
# 9. REMOVE INVALID PRICE RECORDS
# ============================================================

before_invalid_price = df.count()

df = df.filter(
    col("price").isNotNull() &
    (col("price") >= 0)
)

after_invalid_price = df.count()

print("\n========== INVALID PRICE REMOVAL ==========")
print("Records before removing invalid prices:",
      before_invalid_price)

print("Records after removing invalid prices:",
      after_invalid_price)

print("Invalid price records removed:",
      before_invalid_price - after_invalid_price)


# ============================================================
# 10. DATA QUALITY VALIDATION
# ============================================================

print("\n========== DATA QUALITY VALIDATION ==========")


# ------------------------------------------------------------
# Missing values
# ------------------------------------------------------------

missing_id = df.filter(
    col("id").isNull()
).count()

missing_name = df.filter(
    col("name").isNull()
).count()

missing_brand = df.filter(
    col("brand").isNull()
).count()

missing_categories = df.filter(
    col("categories").isNull()
).count()

missing_price = df.filter(
    col("price").isNull()
).count()


print("\nMissing values:")
print("ID:", missing_id)
print("Name:", missing_name)
print("Brand:", missing_brand)
print("Categories:", missing_categories)
print("Price:", missing_price)


# ------------------------------------------------------------
# Duplicate ID check
# ------------------------------------------------------------

duplicate_ids = (
    df.groupBy("id")
      .count()
      .filter(col("count") > 1)
      .count()
)

print("\nDuplicate IDs found:", duplicate_ids)

if duplicate_ids > 0:
    print(
        "Note: Duplicate IDs are reported for validation "
        "but are not removed because the complete records "
        "may contain different product information."
    )


# ------------------------------------------------------------
# Invalid price check
# ------------------------------------------------------------

invalid_prices = df.filter(
    col("price").isNull() |
    (col("price") < 0)
).count()

print("Invalid prices:", invalid_prices)


# ============================================================
# 11. VALIDATION RESULT
# ============================================================

print("\n========== VALIDATION RESULT ==========")

if (
    missing_id == 0
    and missing_name == 0
    and missing_brand == 0
    and missing_categories == 0
    and missing_price == 0
    and invalid_prices == 0
):
    print("DATA QUALITY VALIDATION PASSED")
else:
    print("DATA QUALITY VALIDATION REQUIRES ATTENTION")


# ============================================================
# 12. FINAL RECORD COUNT
# ============================================================

print("\n========== CLEANED RECORD COUNT ==========")

print("Final records:", df.count())


# ============================================================
# 13. FINAL SCHEMA
# ============================================================

print("\n========== FINAL SCHEMA ==========")

df.printSchema()


# ============================================================
# 14. CLEANED SAMPLE DATA
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