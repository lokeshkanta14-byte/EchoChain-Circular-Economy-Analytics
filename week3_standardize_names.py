import os
import re
import pandas as pd


# ============================================================
# ECHOCHAIN - WEEK 3
# COMMIT 2: PRODUCT NAME STANDARDIZATION
# ============================================================


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_PATH = (
    r"C:\Users\M.Alogy"
    r"\EchoChain Circular Economy & Secondary Market Lifecycle Analytics"
)


# ============================================================
# INPUT / OUTPUT
# ============================================================

INPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_prepared_silver.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_standardized_names.csv"
)


# ============================================================
# START
# ============================================================

print("\n==============================================")
print("ECHOCHAIN - WEEK 3")
print("COMMIT 2")
print("PRODUCT NAME STANDARDIZATION")
print("==============================================")


# ============================================================
# CHECK INPUT
# ============================================================

print("\n========== INPUT FILE CHECK ==========")

print("Input:")
print(INPUT_FILE)

if not os.path.isfile(INPUT_FILE):

    raise FileNotFoundError(
        "week3_prepared_silver.csv was not found."
    )

print("Input file found.")


# ============================================================
# READ DATA
# ============================================================

print("\n========== READ PREPARED SILVER ==========")

df = pd.read_csv(
    INPUT_FILE
)

print(
    "Records loaded:",
    len(df)
)

print(
    "Columns:"
)

for column in df.columns:
    print(column)


# ============================================================
# CHECK NAME COLUMN
# ============================================================

if "name" not in df.columns:

    raise ValueError(
        "Product name column 'name' was not found."
    )


# ============================================================
# PRODUCT NAME STANDARDIZATION FUNCTION
# ============================================================

def standardize_product_name(value):

    if pd.isna(value):

        return ""

    value = str(value)

    # Convert to lowercase
    value = value.lower()

    # Replace common separators with spaces
    value = re.sub(
        r"[/_|]+",
        " ",
        value
    )

    # Remove punctuation
    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    # Remove extra whitespace
    value = re.sub(
        r"\s+",
        " ",
        value
    )

    # Remove leading/trailing spaces
    value = value.strip()

    return value


# ============================================================
# STANDARDIZE PRODUCT NAMES
# ============================================================

print("\n========== STANDARDIZING PRODUCT NAMES ==========")

df["standardized_product_name"] = (
    df["name"]
    .apply(standardize_product_name)
)

print(
    "Product names standardized."
)


# ============================================================
# CREATE FUZZY MATCH TEXT
# ============================================================

print("\n========== CREATE FUZZY MATCH FIELD ==========")

df["fuzzy_match_name"] = (
    df["standardized_product_name"]
)

print(
    "Created fuzzy_match_name."
)


# ============================================================
# VALIDATION
# ============================================================

print("\n========== VALIDATION ==========")

empty_standardized = (
    df["standardized_product_name"]
    .eq("")
    .sum()
)

print(
    "Empty standardized names:",
    empty_standardized
)

print(
    "Total records:",
    len(df)
)


# ============================================================
# DISPLAY SAMPLE
# ============================================================

print("\n========== BEFORE / AFTER SAMPLE ==========")

sample_columns = [
    "name",
    "standardized_product_name",
    "fuzzy_match_name"
]

print(
    df[sample_columns]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# SAVE OUTPUT
# ============================================================

print("\n========== WRITE OUTPUT ==========")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "Standardized dataset saved successfully."
)

print(
    "Output:"
)

print(
    OUTPUT_FILE
)


# ============================================================
# VERIFY OUTPUT
# ============================================================

print("\n========== OUTPUT VERIFICATION ==========")

verify_df = pd.read_csv(
    OUTPUT_FILE
)

print(
    "Input records:",
    len(df)
)

print(
    "Output records:",
    len(verify_df)
)

if len(df) == len(verify_df):

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
# FINAL SUCCESS
# ============================================================

print(
    "\n=============================================="
)

print(
    "WEEK 3 COMMIT 2 COMPLETED SUCCESSFULLY"
)

print(
    "=============================================="
)

print(
    "\nOutput file:"
)

print(
    OUTPUT_FILE
)

print(
    "\nProduct names are now standardized"
)

print(
    "and ready for fuzzy matching."
)