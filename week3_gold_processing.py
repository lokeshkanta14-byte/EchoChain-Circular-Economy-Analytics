import os
import pandas as pd

# ============================================================
# ECHOCHAIN - WEEK 3
# COMMIT 5: FINAL GOLD-READY PROCESSING
# ============================================================

PROJECT_PATH = (
    r"C:\Users\M.Alogy"
    r"\EchoChain Circular Economy & Secondary Market Lifecycle Analytics"
)

INPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_fuzzy_matched.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_gold_ready.csv"
)


# ============================================================
# START
# ============================================================

print("\n==============================================")
print("ECHOCHAIN - WEEK 3")
print("COMMIT 5")
print("FINAL GOLD-READY PROCESSING")
print("==============================================")


# ============================================================
# INPUT FILE CHECK
# ============================================================

print("\n========== INPUT FILE CHECK ==========")

print("Input file:")
print(INPUT_FILE)

if not os.path.isfile(INPUT_FILE):

    raise FileNotFoundError(
        "week3_fuzzy_matched.csv was not found."
    )

print("Input file found successfully.")


# ============================================================
# READ FUZZY-MATCHED DATA
# ============================================================

print("\n========== READ FUZZY-MATCHED DATA ==========")

df = pd.read_csv(
    INPUT_FILE
)

input_count = len(df)

print(
    "Input records:",
    input_count
)


# ============================================================
# REQUIRED INPUT COLUMN VALIDATION
# ============================================================

print(
    "\n========== REQUIRED COLUMN VALIDATION =========="
)

required_columns = [
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "sku",
    "sku_clean",
    "standardized_product_name",
    "fuzzy_match_name",
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id",
    "sku_match_available"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    raise ValueError(
        "Missing required columns: "
        + str(missing_columns)
    )

print(
    "All required input columns are available."
)


# ============================================================
# SELECT GOLD-READY FIELDS
# ============================================================

print(
    "\n========== SELECT GOLD FIELDS =========="
)

gold_columns = [
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "sku",
    "sku_clean",
    "standardized_product_name",
    "fuzzy_match_name",
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id",
    "sku_match_available"
]

gold_df = df[
    gold_columns
].copy()

print(
    "Gold fields selected:",
    len(gold_columns)
)


# ============================================================
# FINAL TEXT CLEANING
# ============================================================

print(
    "\n========== FINAL TEXT CLEANING =========="
)

text_columns = [
    "name",
    "brand",
    "categories",
    "sku",
    "sku_clean",
    "standardized_product_name",
    "fuzzy_match_name",
    "matched_product_name",
    "match_status",
    "match_group_id"
]

for column in text_columns:

    gold_df[column] = (
        gold_df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )

print(
    "Text fields cleaned."
)


# ============================================================
# CLEAN PRICE
# ============================================================

print(
    "Cleaning price field..."
)

gold_df["price"] = pd.to_numeric(
    gold_df["price"],
    errors="coerce"
)

print(
    "Price field cleaned."
)


# ============================================================
# CLEAN MATCH SCORE
# ============================================================

print(
    "Cleaning match score..."
)

gold_df["match_score"] = pd.to_numeric(
    gold_df["match_score"],
    errors="coerce"
)

gold_df["match_score"] = (
    gold_df["match_score"]
    .fillna(0)
    .round(2)
)

print(
    "Match score cleaned."
)


# ============================================================
# VALIDATE SKU AVAILABILITY
# ============================================================

print(
    "Validating SKU availability..."
)

gold_df["sku_match_available"] = (
    gold_df["sku_clean"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
)

print(
    "SKU availability validated."
)


# ============================================================
# RECORD PRESERVATION VALIDATION
# ============================================================

print(
    "\n========== RECORD PRESERVATION VALIDATION =========="
)

print(
    "Records before Gold processing:",
    input_count
)

print(
    "Records after field processing:",
    len(gold_df)
)

if len(gold_df) == input_count:

    print(
        "Record preservation validation: PASSED"
    )

else:

    raise ValueError(
        "Record count changed during Gold processing."
    )


# ============================================================
# CREATE UNIQUE GOLD RECORD ID
# ============================================================

print(
    "\n========== CREATE GOLD RECORD ID =========="
)

gold_df.insert(
    0,
    "gold_record_id",
    [
        "ECHO-GOLD-"
        + str(number).zfill(6)
        for number in range(
            1,
            len(gold_df) + 1
        )
    ]
)

print(
    "Gold record IDs created:",
    len(gold_df)
)


# ============================================================
# FINAL NULL VALIDATION
# ============================================================

print(
    "\n========== FINAL NULL VALIDATION =========="
)

important_columns = [
    "gold_record_id",
    "id",
    "standardized_product_name",
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id"
]

null_counts = (
    gold_df[
        important_columns
    ]
    .isna()
    .sum()
)

total_important_nulls = int(
    null_counts.sum()
)

print(
    "Important-field null count:",
    total_important_nulls
)


# ============================================================
# FUZZY MATCH STATISTICS
# ============================================================

print(
    "\n========== GOLD MATCH STATISTICS =========="
)

print(
    "HIGH matches:",
    (
        gold_df["match_status"]
        == "HIGH"
    ).sum()
)

print(
    "POTENTIAL matches:",
    (
        gold_df["match_status"]
        == "POTENTIAL"
    ).sum()
)

print(
    "NO_MATCH records:",
    (
        gold_df["match_status"]
        == "NO_MATCH"
    ).sum()
)

print(
    "Unique match groups:",
    gold_df[
        "match_group_id"
    ].nunique()
)


# ============================================================
# DISPLAY GOLD-READY SAMPLE
# ============================================================

print(
    "\n========== GOLD-READY SAMPLE =========="
)

sample_columns = [
    "gold_record_id",
    "id",
    "standardized_product_name",
    "sku_clean",
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id"
]

print(
    gold_df[
        sample_columns
    ]
    .head(10)
    .to_string(
        index=False
    )
)


# ============================================================
# WRITE GOLD-READY OUTPUT
# ============================================================

print(
    "\n========== WRITE GOLD-READY OUTPUT =========="
)

gold_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "Gold-ready dataset saved successfully."
)

print(
    "Output:"
)

print(
    OUTPUT_FILE
)


# ============================================================
# OUTPUT VERIFICATION
# ============================================================

print(
    "\n========== OUTPUT VERIFICATION =========="
)

verify_df = pd.read_csv(
    OUTPUT_FILE
)

output_count = len(
    verify_df
)

print(
    "Input records:",
    input_count
)

print(
    "Output records:",
    output_count
)

if input_count == output_count:

    print(
        "Record-count validation: PASSED"
    )

else:

    print(
        "Record-count validation: FAILED"
    )

    raise ValueError(
        "Input and output record counts do not match."
    )


# ============================================================
# FINAL GOLD COLUMN VALIDATION
# ============================================================

print(
    "\n========== FINAL COLUMN VALIDATION =========="
)

required_gold_columns = [
    "gold_record_id",
    "id",
    "name",
    "brand",
    "categories",
    "price",
    "sku",
    "sku_clean",
    "standardized_product_name",
    "fuzzy_match_name",
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id",
    "sku_match_available"
]

missing_gold_columns = [
    column
    for column in required_gold_columns
    if column not in verify_df.columns
]

if missing_gold_columns:

    raise ValueError(
        "Missing Gold columns: "
        + str(missing_gold_columns)
    )

print(
    "All Gold-ready columns validated."
)


# ============================================================
# FINAL RECORD COUNT CHECK
# ============================================================

if len(verify_df) != 5434:

    raise ValueError(
        "Expected 5434 records, but found "
        + str(len(verify_df))
    )

print(
    "Expected 5434-record validation: PASSED"
)


# ============================================================
# FINAL SUCCESS
# ============================================================

print(
    "\n=============================================="
)

print(
    "WEEK 3 COMMIT 5 COMPLETED SUCCESSFULLY"
)

print(
    "=============================================="
)

print(
    "\nFinal Gold-ready output:"
)

print(
    OUTPUT_FILE
)

print(
    "\nRecords ready for Gold processing:",
    len(verify_df)
)

print(
    "\nThe dataset is ready for"
)

print(
    "Silver -> Gold Delta processing in Databricks."
)

print(
    "\n=============================================="
)