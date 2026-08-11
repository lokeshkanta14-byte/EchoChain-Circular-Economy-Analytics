from pyspark.sql import SparkSession

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
# 4. REMOVE RECORDS WITH MISSING ID
# ============================================================

before_missing_id = df.count()

df = df.filter(df["id"].isNotNull())

after_missing_id = df.count()

print("\n========== MISSING ID REMOVAL ==========")
print("Records before removing missing IDs:", before_missing_id)
print("Records after removing missing IDs:", after_missing_id)
print("Records removed:", before_missing_id - after_missing_id)


# ============================================================
# 5. FINAL RECORD COUNT
# ============================================================

print("\n========== CLEANED RECORD COUNT ==========")
print(df.count())


# ============================================================
# 6. SCHEMA
# ============================================================

print("\n========== SCHEMA ==========")
df.printSchema()


# ============================================================
# 7. SAMPLE CLEANED DATA
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