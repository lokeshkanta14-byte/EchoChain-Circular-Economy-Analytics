import os
import re
import pandas as pd

# ============================================================
# ECHOCHAIN - WEEK 3
# COMMIT 4: FUZZY PRODUCT MATCHING
# ============================================================

PROJECT_PATH = (
    r"C:\Users\M.Alogy"
    r"\EchoChain Circular Economy & Secondary Market Lifecycle Analytics"
)

INPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_sku_prepared.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_PATH,
    "week3_fuzzy_matched.csv"
)


# ============================================================
# START
# ============================================================

print("\n==============================================")
print("ECHOCHAIN - WEEK 3")
print("COMMIT 4")
print("FUZZY PRODUCT MATCHING")
print("==============================================")


# ============================================================
# CHECK RAPIDFUZZ
# ============================================================

try:

    from rapidfuzz import process, fuzz

except ImportError:

    print("\nRapidFuzz is not installed.")

    print(
        "Run this command:"
    )

    print(
        "python -m pip install rapidfuzz"
    )

    raise


# ============================================================
# INPUT FILE CHECK
# ============================================================

print("\n========== INPUT FILE CHECK ==========")

print("Input:")
print(INPUT_FILE)

if not os.path.isfile(INPUT_FILE):

    raise FileNotFoundError(
        "week3_sku_prepared.csv was not found."
    )

print("Input file found.")


# ============================================================
# READ DATA
# ============================================================

print("\n========== READ SKU-PREPARED DATA ==========")

df = pd.read_csv(
    INPUT_FILE
)

print(
    "Records loaded:",
    len(df)
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "id",
    "name",
    "brand",
    "sku",
    "sku_clean",
    "standardized_product_name",
    "fuzzy_match_name"
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
    "All required columns are available."
)


# ============================================================
# NORMALIZE PRODUCT NAME FOR MATCHING
# ============================================================

print("\n========== PREPARE MATCHING TEXT ==========")


def normalize_for_matching(value):

    if pd.isna(value):

        return ""

    value = str(value).lower()

    # Normalize GB values
    value = re.sub(
        r"(\d+)\s*gb",
        r"\1gb",
        value
    )

    # Replace punctuation with spaces
    value = re.sub(
        r"[^a-z0-9\s]",
        " ",
        value
    )

    # Remove extra spaces
    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


df["match_text"] = (
    df["standardized_product_name"]
    .apply(normalize_for_matching)
)

print(
    "Matching text prepared."
)


# ============================================================
# GET UNIQUE PRODUCT NAMES
# ============================================================

print("\n========== PREPARE PRODUCT NAME LIST ==========")

unique_names = (
    df["match_text"]
    .dropna()
    .unique()
    .tolist()
)

print(
    "Unique product names:",
    len(unique_names)
)


# ============================================================
# FUZZY MATCH CONFIGURATION
# ============================================================

FUZZY_THRESHOLD = 90

print(
    "Fuzzy matching threshold:",
    FUZZY_THRESHOLD
)


# ============================================================
# MATCH CACHE
# ============================================================

match_cache = {}


# ============================================================
# FIND BEST MATCH
# ============================================================

def find_best_match(product_name):

    if not product_name:

        return (
            "",
            0
        )

    # Use cached result if already calculated
    if product_name in match_cache:

        return match_cache[
            product_name
        ]

    results = process.extract(
        product_name,
        unique_names,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=FUZZY_THRESHOLD,
        limit=2
    )

    # No fuzzy match found
    if not results:

        result = (
            product_name,
            100.0
        )

        match_cache[
            product_name
        ] = result

        return result

    best_name = results[0][0]

    best_score = results[0][1]

    result = (
        best_name,
        round(
            float(best_score),
            2
        )
    )

    match_cache[
        product_name
    ] = result

    return result


# ============================================================
# RUN FUZZY MATCHING
# ============================================================

print("\n========== FUZZY MATCHING ==========")

print(
    "Matching product names..."
)

match_results = []

total_records = len(df)

for index, product_name in enumerate(
    df["match_text"]
):

    best_name, score = (
        find_best_match(
            product_name
        )
    )

    match_results.append(
        (
            best_name,
            score
        )
    )

    if (index + 1) % 500 == 0:

        print(
            "Processed:",
            index + 1,
            "/",
            total_records
        )


# ============================================================
# ADD MATCH RESULTS
# ============================================================

df["matched_product_name"] = [
    result[0]
    for result in match_results
]

df["match_score"] = [
    result[1]
    for result in match_results
]


# ============================================================
# CLASSIFY MATCH
# ============================================================

print("\n========== MATCH CLASSIFICATION ==========")


def classify_match(score):

    if score >= 95:

        return "HIGH"

    elif score >= 90:

        return "POTENTIAL"

    else:

        return "NO_MATCH"


df["match_status"] = (
    df["match_score"]
    .apply(classify_match)
)


# ============================================================
# CREATE MATCH GROUP ID
# ============================================================

print(
    "Creating match group IDs..."
)

group_mapping = {}

group_counter = 1

match_group_ids = []

for product_name in df[
    "matched_product_name"
]:

    if product_name not in group_mapping:

        group_mapping[
            product_name
        ] = (
            "ECHO-G"
            + str(group_counter).zfill(5)
        )

        group_counter += 1

    match_group_ids.append(
        group_mapping[
            product_name
        ]
    )


df["match_group_id"] = (
    match_group_ids
)


# ============================================================
# SKU MATCH AVAILABILITY
# ============================================================

print(
    "Creating SKU availability flag..."
)

df["sku_match_available"] = (
    df["sku_clean"]
    .fillna("")
    .astype(str)
    .str.strip()
    .ne("")
)


# ============================================================
# MATCH STATISTICS
# ============================================================

print("\n========== MATCH STATISTICS ==========")

print(
    "Total records:",
    len(df)
)

print(
    "Unique product names:",
    df["match_text"].nunique()
)

print(
    "Unique match groups:",
    df["match_group_id"].nunique()
)

print(
    "High-confidence matches:",
    (
        df["match_status"] == "HIGH"
    ).sum()
)

print(
    "Potential matches:",
    (
        df["match_status"] == "POTENTIAL"
    ).sum()
)

print(
    "No-match records:",
    (
        df["match_status"] == "NO_MATCH"
    ).sum()
)


# ============================================================
# DISPLAY SAMPLE
# ============================================================

print("\n========== FUZZY MATCH SAMPLE ==========")

sample_columns = [
    "name",
    "sku_clean",
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id"
]

print(
    df[
        sample_columns
    ]
    .head(10)
    .to_string(
        index=False
    )
)


# ============================================================
# WRITE OUTPUT
# ============================================================

print("\n========== WRITE FUZZY MATCH OUTPUT ==========")

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    "Fuzzy matched dataset saved successfully."
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
# VALIDATE OUTPUT COLUMNS
# ============================================================

required_output_columns = [
    "matched_product_name",
    "match_score",
    "match_status",
    "match_group_id",
    "sku_match_available"
]

missing_output_columns = [
    column
    for column in required_output_columns
    if column not in verify_df.columns
]

if missing_output_columns:

    raise ValueError(
        "Missing fuzzy matching output columns: "
        + str(missing_output_columns)
    )

print(
    "Fuzzy matching output columns validated."
)


# ============================================================
# FINAL SUCCESS
# ============================================================

print(
    "\n=============================================="
)

print(
    "WEEK 3 COMMIT 4 COMPLETED SUCCESSFULLY"
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
    "\nFuzzy-matched data is now ready"
)

print(
    "for the final Gold-ready processing stage."
)