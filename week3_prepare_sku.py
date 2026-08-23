import os
import re
import pandas as pd

# ============================================================
# ECHOCHAIN - WEEK 3
# COMMIT 3: SKU PREPARATION
# ============================================================

PROJECT_PATH = (
    r"C:\Users\M.Alogy"
    r"\EchoChain Circular Economy & Secondary Market Lifecycle Analytics"
)

INPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_standardized_names.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_sku_prepared.csv"
)

print("\n==============================================")
print("ECHOCHAIN - WEEK 3")
print("COMMIT 3")
print("SKU PREPARATION")
print("==============================================")


# ============================================================
# CHECK INPUT
# ============================================================

print("\n========== INPUT FILE CHECK ==========")

print("Input:")
print(INPUT_FILE)

if not os.path.isfile(INPUT_FILE):
    raise FileNotFoundError(
        "week3_standardized_names.csv was not found."
    )

print("Input file found.")


# ============================================================
# READ DATA
# ============================================================

print("\n========== READ STANDARDIZED DATA ==========")

df = pd.read_csv(INPUT_FILE)

print(
    "Records loaded:",
    len(df)
)


# ============================================================
# CHECK SKU COLUMN
# ============================================================

if "sku" not in df.columns:

    raise ValueError(
        "SKU column was not found in the dataset."
    )

print(
    "SKU column found."
)


# ============================================================
# SKU CLEANING FUNCTION
# ============================================================

def clean_sku(value):

    if pd.isna(value):
        return ""

    value = str(value).strip()

    # Convert to uppercase
    value = value.upper()

    # Remove spaces
    value = re.sub(
        r"\s+",
        "",
        value
    )

    # Remove common separators
    value = re.sub(
        r"[-_/]+",
        "",
        value
    )

    # Keep only letters and numbers
    value = re.sub(
        r"[^A-Z0-9]",
        "",
        value
    )

    return value


# ============================================================
# PREPARE SKU
# ============================================================

print("\n========== SKU STANDARDIZATION ==========")

df["sku_clean"] = (
    df["sku"]
    .apply(clean_sku)
)

print(
    "SKU cleaning completed."
)


# ============================================================
# SKU VALIDATION
# ============================================================

print("\n========== SKU VALIDATION ==========")

empty_sku_count = (
    df["sku_clean"]
    .eq("")
    .sum()
)

valid_sku_count = (
    len(df) - empty_sku_count
)

print(
    "Total records:",
    len(df)
)

print(
    "Valid SKU records:",
    valid_sku_count
)

print(
    "Empty SKU records:",
    empty_sku_count
)


# ============================================================
# SKU LENGTH
# ============================================================

df["sku_length"] = (
    df["sku_clean"]
    .str.len()
)


# ============================================================
# SKU AVAILABILITY FLAG
# ============================================================

df["sku_available"] = (
    df["sku_clean"]
    .ne("")
)


# ============================================================
# DISPLAY SAMPLE
# ============================================================

print("\n========== SKU SAMPLE ==========")

sample_columns = [
    "name",
    "sku",
    "sku_clean",
    "sku_length",
    "sku_available"
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
    "SKU-prepared dataset saved successfully."
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
# REQUIRED OUTPUT COLUMNS
# ============================================================

required_output_columns = [
    "sku",
    "sku_clean",
    "sku_length",
    "sku_available"
]

missing_output_columns = [
    column
    for column in required_output_columns
    if column not in verify_df.columns
]

if missing_output_columns:

    raise ValueError(
        "Missing output columns: "
        + str(missing_output_columns)
    )

print(
    "Required SKU output columns validated."
)


# ============================================================
# FINAL SUCCESS
# ============================================================

print(
    "\n=============================================="
)

print(
    "WEEK 3 COMMIT 3 COMPLETED SUCCESSFULLY"
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
    "\nSKU data is now prepared for"
)

print(
    "fuzzy matching and Gold-layer processing."
)