import os

# ============================================================
# ECHOCHAIN - WEEK 3
# COMMIT 1: PREPARE SILVER DATA FOR FUZZY MATCHING
# ============================================================

# ============================================================
# WINDOWS / PYTHON CONFIGURATION
# ============================================================

HADOOP_HOME = r"C:\hadoop"

PYTHON_PATH = (
    r"C:\Users\M.Alogy\AppData\Local\Programs"
    r"\Python\Python313\python.exe"
)

os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME

os.environ["PYSPARK_PYTHON"] = PYTHON_PATH
os.environ["PYSPARK_DRIVER_PYTHON"] = PYTHON_PATH


# ============================================================
# IMPORTS
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_PATH = (
    r"C:\Users\M.Alogy"
    r"\EchoChain Circular Economy & Secondary Market Lifecycle Analytics"
)


# ============================================================
# EXISTING SILVER PARQUET
# ============================================================

SILVER_FILE = os.path.join(
    PROJECT_PATH,
    "silver_electronics_products",
    "part-00000-66166b43-71c9-49ee-946e-0c3acad5d37e-c000.parquet"
)


# ============================================================
# WEEK 3 OUTPUT
# ============================================================

OUTPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_prepared_silver.csv"
)


# ============================================================
# START
# ============================================================

print("\n==============================================")
print("ECHOCHAIN - WEEK 3")
print("COMMIT 1")
print("PREPARE SILVER DATA FOR FUZZY MATCHING")
print("==============================================")


# ============================================================
# CHECK SILVER FILE
# ============================================================

print("\n========== SILVER FILE CHECK ==========")

print(
    "Silver Parquet:"
)

print(
    SILVER_FILE
)

if not os.path.isfile(SILVER_FILE):

    raise FileNotFoundError(
        "Silver Parquet file was not found."
    )

print(
    "Silver Parquet file found."
)


# ============================================================
# CREATE SPARK SESSION
# ============================================================

print("\n========== STARTING SPARK ==========")

spark = (
    SparkSession.builder
    .appName("EchoChain Week 3 Commit 1")
    .master("local[2]")
    .config(
        "spark.driver.memory",
        "2g"
    )
    .config(
        "spark.hadoop.home.dir",
        HADOOP_HOME
    )
    .config(
        "spark.hadoop.fs.file.impl",
        "org.apache.hadoop.fs.RawLocalFileSystem"
    )
    .config(
        "spark.hadoop.io.native.lib.available",
        "false"
    )
    .config(
        "spark.sql.shuffle.partitions",
        "2"
    )
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print(
    "Spark started successfully."
)


# ============================================================
# READ SILVER PARQUET
# ============================================================

print("\n========== READ SILVER DATA ==========")

silver_df = (
    spark.read
    .format("parquet")
    .load(SILVER_FILE)
)

print(
    "Silver Parquet loaded successfully."
)


# ============================================================
# RECORD COUNT
# ============================================================

silver_count = silver_df.count()

print(
    "Silver records:",
    silver_count
)

if silver_count == 5434:

    print(
        "Silver record-count validation: PASSED"
    )

else:

    print(
        "Silver record-count validation: WARNING"
    )


# ============================================================
# REQUIRED COLUMNS
# ============================================================

print("\n========== REQUIRED COLUMN VALIDATION ==========")

required_columns = [
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "sku"
]

missing_columns = [
    column
    for column in required_columns
    if column not in silver_df.columns
]

if missing_columns:

    print(
        "Missing columns:",
        missing_columns
    )

    spark.stop()

    raise ValueError(
        "Required columns are missing."
    )

print(
    "All required columns are available."
)


# ============================================================
# SELECT REQUIRED FIELDS
# ============================================================

print("\n========== SELECT WEEK 3 FIELDS ==========")

df = silver_df.select(
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "sku"
)

print(
    "Selected fields:"
)

for column in df.columns:

    print(
        column
    )


# ============================================================
# REMOVE EMPTY PRODUCT NAMES
# ============================================================

print("\n========== PRODUCT NAME VALIDATION ==========")

df = df.filter(
    col("name").isNotNull()
)

df = df.filter(
    trim(col("name")) != ""
)

print(
    "Product name validation completed."
)


# ============================================================
# TRIM TEXT FIELDS
# ============================================================

print("\n========== TEXT CLEANING ==========")

df = (
    df
    .withColumn(
        "name",
        trim(col("name"))
    )
    .withColumn(
        "brand",
        trim(col("brand"))
    )
    .withColumn(
        "categories",
        trim(col("categories"))
    )
    .withColumn(
        "sku",
        trim(col("sku"))
    )
)

print(
    "Trimmed product names."
)

print(
    "Trimmed brand values."
)

print(
    "Trimmed category values."
)

print(
    "Trimmed SKU values."
)


# ============================================================
# CREATE NORMALIZED PRODUCT NAME
# ============================================================

print("\n========== PRODUCT NAME NORMALIZATION ==========")

df = df.withColumn(
    "product_name_lower",
    lower(col("name"))
)

print(
    "Created product_name_lower."
)


# ============================================================
# FINAL COUNT
# ============================================================

print("\n========== FINAL PREPARED RECORD COUNT ==========")

final_count = df.count()

print(
    "Prepared records:",
    final_count
)


# ============================================================
# SHOW SAMPLE
# ============================================================

print("\n========== PREPARED DATA SAMPLE ==========")

df.select(
    "id",
    "name",
    "brand",
    "sku",
    "product_name_lower"
).show(
    5,
    truncate=40
)


# ============================================================
# CONVERT TO PANDAS
# ============================================================

print("\n========== PREPARE LOCAL OUTPUT ==========")

print(
    "Converting prepared Spark DataFrame to Pandas..."
)

try:

    pandas_df = df.toPandas()

    print(
        "Pandas conversion completed."
    )

except Exception as e:

    print(
        "\nERROR: Could not convert Spark DataFrame to Pandas."
    )

    print(
        e
    )

    spark.stop()

    raise


# ============================================================
# WRITE CSV USING PYTHON/PANDAS
# ============================================================

print("\n========== WRITE WEEK 3 OUTPUT ==========")

print(
    "Output file:"
)

print(
    OUTPUT_FILE
)

try:

    pandas_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        "\nWeek 3 prepared dataset saved successfully."
    )

except Exception as e:

    print(
        "\nERROR WHILE WRITING CSV:"
    )

    print(
        e
    )

    spark.stop()

    raise


# ============================================================
# VERIFY CSV
# ============================================================

print("\n========== OUTPUT VERIFICATION ==========")

try:

    import pandas as pd

    verify_df = pd.read_csv(
        OUTPUT_FILE
    )

    verify_count = len(
        verify_df
    )

    print(
        "Output records:",
        verify_count
    )

    print(
        "Expected records:",
        final_count
    )

    if verify_count == final_count:

        print(
            "Output record-count validation: PASSED"
        )

    else:

        print(
            "Output record-count validation: FAILED"
        )

except Exception as e:

    print(
        "\nCSV verification failed:"
    )

    print(
        e
    )

    spark.stop()

    raise


# ============================================================
# FINAL SUCCESS
# ============================================================

print(
    "\n=============================================="
)

print(
    "WEEK 3 COMMIT 1 COMPLETED SUCCESSFULLY"
)

print(
    "=============================================="
)

print(
    "\nSilver input records:",
    silver_count
)

print(
    "Prepared records:",
    final_count
)

print(
    "Output records:",
    verify_count
)

print(
    "Output file:",
    OUTPUT_FILE
)

print(
    "\nThe prepared dataset is ready for"
)

print(
    "Week 3 Commit 2 - Product Standardization."
)


# ============================================================
# STOP SPARK
# ============================================================

spark.stop()

print(
    "\nSpark session stopped."
)