import os
import shutil

# ============================================================
# WINDOWS / LOCAL SPARK CONFIGURATION
# ============================================================

HADOOP_HOME = r"C:\hadoop"

PYTHON_PATH = (
    r"C:\Users\M.Alogy\AppData\Local\Programs"
    r"\Python\Python313\python.exe"
)

# ------------------------------------------------------------
# Python configuration
# ------------------------------------------------------------

os.environ["PYSPARK_PYTHON"] = PYTHON_PATH
os.environ["PYSPARK_DRIVER_PYTHON"] = PYTHON_PATH

# ------------------------------------------------------------
# Hadoop configuration
# ------------------------------------------------------------

os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME

# ------------------------------------------------------------
# IMPORTANT:
# Make Hadoop bin available to Java/Hadoop
# ------------------------------------------------------------

HADOOP_BIN = os.path.join(HADOOP_HOME, "bin")

current_path = os.environ.get("PATH", "")

if HADOOP_BIN not in current_path:
    os.environ["PATH"] = HADOOP_BIN + os.pathsep + current_path


# ============================================================
# DISABLE HADOOP NATIVE WINDOWS LIBRARY
# ============================================================
#
# Your previous error was:
#
# NativeIO$Windows.access0
#
# This happens while Spark is writing/committing files.
#
# These settings prevent Hadoop from trying to use the
# problematic native library.
#
# IMPORTANT: They MUST be set BEFORE SparkSession is created.
# ============================================================

os.environ["HADOOP_OPTS"] = (
    "-Dhadoop.native.lib=false "
    "-Dio.native.lib.available=false"
)


# ============================================================
# IMPORTS
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when
from functools import reduce


# ============================================================
# CREATE SPARK SESSION
# ============================================================

print("\n==============================================")
print("STARTING PYSPARK")
print("==============================================")

spark = (
    SparkSession.builder

    .appName(
        "Electronics Products Silver Layer"
    )

    .master("local[2]")

    # --------------------------------------------------------
    # Memory
    # --------------------------------------------------------

    .config(
        "spark.driver.memory",
        "2g"
    )

    # --------------------------------------------------------
    # Windows local filesystem
    # --------------------------------------------------------

    .config(
        "spark.hadoop.fs.file.impl",
        "org.apache.hadoop.fs.RawLocalFileSystem"
    )

    .config(
        "spark.hadoop.home.dir",
        HADOOP_HOME
    )

    # --------------------------------------------------------
    # IMPORTANT: Disable native Hadoop library
    # --------------------------------------------------------

    .config(
        "spark.hadoop.io.native.lib.available",
        "false"
    )

    .config(
        "spark.hadoop.hadoop.native.lib",
        "false"
    )

    # --------------------------------------------------------
    # File permissions
    # --------------------------------------------------------

    .config(
        "spark.hadoop.fs.permissions.umask-mode",
        "000"
    )

    # --------------------------------------------------------
    # File output committer
    # --------------------------------------------------------

    .config(
        "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version",
        "2"
    )

    .config(
        "spark.hadoop.mapreduce.fileoutputcommitter.cleanup-failures.ignored",
        "true"
    )

    # --------------------------------------------------------
    # Reduce local workload
    # --------------------------------------------------------

    .config(
        "spark.sql.shuffle.partitions",
        "2"
    )

    # --------------------------------------------------------
    # Avoid unnecessary compression
    # --------------------------------------------------------

    .config(
        "spark.sql.parquet.compression.codec",
        "uncompressed"
    )

    .getOrCreate()
)


# ============================================================
# LOG LEVEL
# ============================================================

spark.sparkContext.setLogLevel("WARN")


# ============================================================
# INPUT / OUTPUT PATHS
# ============================================================

input_file = "electronics_products_pricing.csv"

# Use a short path to avoid Windows path problems.
silver_output = r"C:\silver_electronics_products"


# ============================================================
# HADOOP INFORMATION
# ============================================================

print("\n========== HADOOP INFORMATION ==========")

try:

    hadoop_version = (
        spark.sparkContext
        ._jvm
        .org.apache.hadoop.util.VersionInfo
        .getVersion()
    )

    print(
        "Hadoop version:",
        hadoop_version
    )

except Exception as e:

    print(
        "Could not determine Hadoop version."
    )

    print(e)


# ============================================================
# HADOOP FILE CHECK
# ============================================================

print("\n========== HADOOP FILE CHECK ==========")

winutils_path = os.path.join(
    HADOOP_HOME,
    "bin",
    "winutils.exe"
)

hadoop_dll_path = os.path.join(
    HADOOP_HOME,
    "bin",
    "hadoop.dll"
)

print(
    "HADOOP_HOME:",
    HADOOP_HOME
)

print(
    "HADOOP_BIN:",
    HADOOP_BIN
)

print(
    "winutils.exe:",
    winutils_path
)

print(
    "hadoop.dll:",
    hadoop_dll_path
)

print(
    "winutils.exe exists:",
    os.path.isfile(winutils_path)
)

print(
    "hadoop.dll exists:",
    os.path.isfile(hadoop_dll_path)
)


# ============================================================
# 1. READ RAW DATA
# ============================================================

print("\n==============================================")
print("1. READ RAW DATA")
print("==============================================")

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(input_file)
)

raw_count = df.count()

print(
    "Total raw records:",
    raw_count
)


# ============================================================
# 2. COLUMN NAMES
# ============================================================

print("\n==============================================")
print("2. COLUMN NAMES")
print("==============================================")

for column in df.columns:
    print(column)


# ============================================================
# 3. REMOVE COMPLETE DUPLICATE RECORDS
# ============================================================

print("\n==============================================")
print("3. DUPLICATE REMOVAL")
print("==============================================")

before_duplicates = df.count()

df = df.dropDuplicates()

after_duplicates = df.count()

duplicates_removed = (
    before_duplicates -
    after_duplicates
)

print(
    "Records before duplicates:",
    before_duplicates
)

print(
    "Records after duplicates:",
    after_duplicates
)

print(
    "Duplicates removed:",
    duplicates_removed
)


# ============================================================
# 4. REMOVE COMPLETELY EMPTY RECORDS
# ============================================================

print("\n==============================================")
print("4. EMPTY ROW REMOVAL")
print("==============================================")

before_empty = df.count()

non_null_conditions = [
    col(f"`{column}`").isNotNull()
    for column in df.columns
]

df = df.filter(
    reduce(
        lambda x, y: x | y,
        non_null_conditions
    )
)

after_empty = df.count()

empty_removed = (
    before_empty -
    after_empty
)

print(
    "Records before empty-row removal:",
    before_empty
)

print(
    "Records after empty-row removal:",
    after_empty
)

print(
    "Empty rows removed:",
    empty_removed
)


# ============================================================
# 5. REMOVE RECORDS WITH MISSING ID
# ============================================================

print("\n==============================================")
print("5. MISSING ID REMOVAL")
print("==============================================")

before_missing_id = df.count()

df = df.filter(
    col("id").isNotNull()
)

after_missing_id = df.count()

missing_id_removed = (
    before_missing_id -
    after_missing_id
)

print(
    "Records before missing-ID removal:",
    before_missing_id
)

print(
    "Records after missing-ID removal:",
    after_missing_id
)

print(
    "Records removed:",
    missing_id_removed
)


# ============================================================
# 6. HANDLE MISSING VALUES
# ============================================================

print("\n==============================================")
print("6. MISSING VALUE HANDLING")
print("==============================================")

df = df.fillna(
    {
        "name": "Unknown",
        "brand": "Unknown",
        "categories": "Unknown"
    }
)

print(
    "name NULL values -> Unknown"
)

print(
    "brand NULL values -> Unknown"
)

print(
    "categories NULL values -> Unknown"
)


# ============================================================
# 7. CLEAN TEXT COLUMNS
# ============================================================

print("\n==============================================")
print("7. TEXT CLEANING")
print("==============================================")

text_columns = [
    "name",
    "brand",
    "categories"
]

for column in text_columns:

    df = df.withColumn(
        column,
        trim(col(column))
    )

print(
    "Trimmed spaces from:",
    ", ".join(text_columns)
)


# ============================================================
# 8. SAFE PRICE TYPE CONVERSION
# ============================================================

print("\n==============================================")
print("8. PRICE TYPE CONVERSION")
print("==============================================")

price_as_string = trim(
    col("price").cast("string")
)

df = df.withColumn(
    "price",

    when(
        price_as_string.rlike(
            r"^-?\d+(\.\d+)?$"
        ),
        price_as_string.cast("double")
    )

    .otherwise(None)
)

print(
    "Price converted to DOUBLE."
)

print(
    "Invalid/non-numeric prices converted to NULL."
)


# ============================================================
# 9. REMOVE INVALID PRICE RECORDS
# ============================================================

print("\n==============================================")
print("9. INVALID PRICE REMOVAL")
print("==============================================")

before_invalid_price = df.count()

df = df.filter(
    col("price").isNotNull()
    &
    (col("price") >= 0)
)

after_invalid_price = df.count()

invalid_prices_removed = (
    before_invalid_price -
    after_invalid_price
)

print(
    "Records before invalid-price removal:",
    before_invalid_price
)

print(
    "Records after invalid-price removal:",
    after_invalid_price
)

print(
    "Invalid price records removed:",
    invalid_prices_removed
)


# ============================================================
# 10. DATA QUALITY VALIDATION
# ============================================================

print("\n==============================================")
print("10. DATA QUALITY VALIDATION")
print("==============================================")

missing_id = (
    df.filter(
        col("id").isNull()
    ).count()
)

missing_name = (
    df.filter(
        col("name").isNull()
    ).count()
)

missing_brand = (
    df.filter(
        col("brand").isNull()
    ).count()
)

missing_categories = (
    df.filter(
        col("categories").isNull()
    ).count()
)

missing_price = (
    df.filter(
        col("price").isNull()
    ).count()
)

print("\nMissing values:")

print(
    "ID:",
    missing_id
)

print(
    "Name:",
    missing_name
)

print(
    "Brand:",
    missing_brand
)

print(
    "Categories:",
    missing_categories
)

print(
    "Price:",
    missing_price
)


# ============================================================
# 11. DUPLICATE ID VALIDATION
# ============================================================

print("\n==============================================")
print("11. DUPLICATE ID VALIDATION")
print("==============================================")

duplicate_ids = (
    df.groupBy("id")
      .count()
      .filter(col("count") > 1)
      .count()
)

print(
    "Duplicate IDs found:",
    duplicate_ids
)

if duplicate_ids > 0:

    print(
        "Duplicate IDs are reported for validation."
    )

    print(
        "They are not removed because different records "
        "may contain different product information."
    )


# ============================================================
# 12. SKU EXTRACTION
# ============================================================

print("\n==============================================")
print("12. SKU EXTRACTION")
print("==============================================")

# Priority:
#
# manufacturerNumber
#       ↓
# asins
#       ↓
# upc
#       ↓
# ean

df = df.withColumn(
    "sku",

    when(
        col("manufacturerNumber").isNotNull()
        &
        (
            trim(
                col("manufacturerNumber")
            ) != ""
        ),
        trim(
            col("manufacturerNumber")
        )
    )

    .when(
        col("asins").isNotNull()
        &
        (
            trim(
                col("asins")
            ) != ""
        ),
        trim(
            col("asins")
        )
    )

    .when(
        col("upc").isNotNull()
        &
        (
            trim(
                col("upc")
            ) != ""
        ),
        trim(
            col("upc")
        )
    )

    .when(
        col("ean").isNotNull()
        &
        (
            trim(
                col("ean")
            ) != ""
        ),
        trim(
            col("ean")
        )
    )

    .otherwise(None)
)


sku_count = (
    df.filter(
        col("sku").isNotNull()
    ).count()
)

print(
    "SKU priority:"
)

print(
    "manufacturerNumber -> ASIN -> UPC -> EAN"
)

print(
    "Records with SKU:",
    sku_count
)


# ============================================================
# 13. FINAL RECORD COUNT
# ============================================================

print("\n==============================================")
print("13. CLEANED RECORD COUNT")
print("==============================================")

final_records = df.count()

print(
    "Final records:",
    final_records
)


# ============================================================
# 14. FINAL SCHEMA
# ============================================================

print("\n==============================================")
print("14. FINAL SCHEMA")
print("==============================================")

df.printSchema()


# ============================================================
# 15. CLEANED SAMPLE DATA
# ============================================================

print("\n==============================================")
print("15. CLEANED SAMPLE DATA")
print("==============================================")

df.select(
    "id",
    "sku",
    "name",
    "brand",
    "categories",
    "price",
    "weight"
).show(
    5,
    truncate=30
)


# ============================================================
# 16. PREPARE SILVER OUTPUT
# ============================================================

print("\n==============================================")
print("16. PREPARE SILVER OUTPUT")
print("==============================================")

print(
    "Silver output:",
    silver_output
)

# ------------------------------------------------------------
# Delete previous output
# ------------------------------------------------------------

if os.path.exists(silver_output):

    print(
        "Previous Silver Layer exists."
    )

    print(
        "Deleting previous output..."
    )

    try:

        shutil.rmtree(
            silver_output
        )

        print(
            "Previous Silver Layer deleted."
        )

    except PermissionError:

        print(
            "\nERROR: Windows has locked the old output."
        )

        print(
            "Close File Explorer if it is open inside:"
        )

        print(
            silver_output
        )

        spark.stop()

        raise

    except Exception as e:

        print(
            "\nERROR while deleting old output:"
        )

        print(e)

        spark.stop()

        raise


# ============================================================
# 17. CREATE SILVER LAYER
# ============================================================

print("\n==============================================")
print("17. SILVER LAYER CREATION")
print("==============================================")

# ------------------------------------------------------------
# Use ONE partition because this is a local internship project.
# ------------------------------------------------------------

silver_df = df.coalesce(1)

print(
    "Number of output partitions:",
    silver_df.rdd.getNumPartitions()
)

print(
    "Writing Parquet..."
)

print(
    "Output:",
    silver_output
)


try:

    (
        silver_df.write
        .mode("overwrite")
        .format("parquet")
        .option(
            "compression",
            "uncompressed"
        )
        .save(silver_output)
    )

    print(
        "\nSUCCESS!"
    )

    print(
        "Silver Layer created successfully."
    )

except Exception as e:

    print(
        "\n=============================================="
    )

    print(
        "SILVER LAYER WRITE FAILED"
    )

    print(
        "=============================================="
    )

    print(
        "\nThe transformation completed,"
    )

    print(
        "but Spark could not complete the Windows "
        "Parquet filesystem write."
    )

    print(
        "\nError:"
    )

    print(e)

    print(
        "\nIf the error contains:"
    )

    print(
        "NativeIO$Windows.access0"
    )

    print(
        "then the C:\\hadoop\\bin native binaries "
        "need to be corrected."
    )

    spark.stop()

    raise


# ============================================================
# 18. VERIFY SILVER LAYER
# ============================================================

print("\n==============================================")
print("18. SILVER LAYER VERIFICATION")
print("==============================================")

try:

    silver_check = (
        spark.read
        .format("parquet")
        .load(silver_output)
    )

    silver_count = silver_check.count()

    print(
        "Silver Layer records:",
        silver_count
    )

    print(
        "Expected records:",
        final_records
    )

    # --------------------------------------------------------
    # Record count validation
    # --------------------------------------------------------

    if silver_count == final_records:

        print(
            "\nRecord count validation: PASSED"
        )

    else:

        print(
            "\nRecord count validation: FAILED"
        )

        print(
            "Expected:",
            final_records
        )

        print(
            "Actual:",
            silver_count
        )


    # --------------------------------------------------------
    # Display Silver data
    # --------------------------------------------------------

    print(
        "\nSilver Layer sample:"
    )

    silver_check.select(
        "id",
        "sku",
        "name",
        "brand",
        "categories",
        "price"
    ).show(
        5,
        truncate=30
    )


except Exception as e:

    print(
        "\nSilver Layer was created, "
        "but verification failed."
    )

    print(e)

    spark.stop()

    raise


# ============================================================
# 19. FINAL SUMMARY
# ============================================================

print("\n==============================================")
print("SILVER LAYER PROCESS COMPLETED SUCCESSFULLY")
print("==============================================")

print(
    "\nRaw records:",
    raw_count
)

print(
    "Duplicates removed:",
    duplicates_removed
)

print(
    "Empty rows removed:",
    empty_removed
)

print(
    "Missing IDs removed:",
    missing_id_removed
)

print(
    "Invalid prices removed:",
    invalid_prices_removed
)

print(
    "Records with SKU:",
    sku_count
)

print(
    "Final Silver records:",
    final_records
)

print(
    "Silver Layer path:",
    silver_output
)

print(
    "Format: PARQUET"
)


# ============================================================
# 20. STOP SPARK
# ============================================================

spark.stop()

print(
    "\nSpark session stopped."
)

print(
    "Project completed successfully."
)