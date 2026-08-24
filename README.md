# EchoChain – Circular Economy & Secondary Market Lifecycle Analytics

EchoChain is a data engineering and analytics project focused on processing and transforming electronics product data to support analysis of the secondary market lifecycle.

The project follows a layered data-processing approach using PySpark, with the cleaned data prepared for further transformation, matching, and analytics.

---

## Technology Stack

- Python
- PySpark
- SQL
- Databricks
- Git & GitHub
- Parquet
- Delta Lake

---

# Week 1 – Data Preparation and Silver Layer

During Week 1, the raw electronics product dataset was processed locally using PySpark to create a cleaned Silver dataset.

## Tasks Completed

- Loaded the raw electronics product CSV dataset.
- Inspected the dataset structure and column names.
- Removed complete duplicate records.
- Removed completely empty records.
- Removed records with missing product IDs.
- Handled missing values in product name, brand, and categories.
- Cleaned product text fields by removing extra spaces.
- Converted price values to numeric format.
- Removed invalid and negative price records.
- Performed data quality validation.
- Checked for duplicate product IDs.
- Extracted SKU values using the following priority:
  - `manufacturerNumber`
  - `ASIN`
  - `UPC`
  - `EAN`
- Created the cleaned Silver Layer in Parquet format.
- Verified the Silver Layer record count and sample data.

## Week 1 Results

| Metric | Result |
|---|---:|
| Raw Records | 5,436 |
| Final Silver Records | 5,434 |
| Invalid Price Records Removed | 2 |
| Output Format | Parquet |

---

# Week 2 – Bronze to Silver Transformation

During Week 2, the existing Bronze data was continued through the PySpark transformation stage to prepare the cleaned Silver dataset.

## Tasks Completed

- Used the existing Bronze electronics product data.
- Processed the data using PySpark.
- Cleaned product names and text fields.
- Removed duplicate records.
- Handled missing and invalid values.
- Standardized price-related data.
- Extracted SKU values from available product identifiers.
- Performed initial data quality validation.
- Prepared the transformed dataset as Silver data.
- Validated the final Silver record count.
- Generated the Silver output in Parquet format.

## Silver Dataset

The resulting Silver dataset contains:

**5,434 records**

The Silver dataset was prepared for the next stage of the project, including product/SKU standardization, fuzzy matching, and Gold-layer processing.

---

# Data Pipeline

```text
Raw Electronics Data
        |
        v
Bronze Layer
        |
        v
PySpark Data Cleaning
        |
        v
Silver Layer
        |
        v
Product & SKU Transformation
        |
        v
Fuzzy Matching
        |
        v
Gold Layer
        |
        v
Analytics


## Week 3 – Silver to Gold Data Preparation

### Objective

Prepare the cleaned Silver-layer electronics product data for Gold-layer processing and downstream fuzzy matching.

### Week 3 Activities

#### 1. Prepare Silver Data

- Loaded the Silver electronics product dataset.
- Validated the required product columns.
- Selected the fields required for downstream processing.
- Validated product names and record counts.
- Prepared the dataset for fuzzy matching.

#### 2. Standardize Product Names

- Cleaned and standardized product names.
- Converted product names into a consistent format.
- Removed unnecessary variations in product-name text.
- Generated `week3_standardized_names.csv`.
- Validated all 5,434 records.

#### 3. Prepare and Standardize SKU Data

- Cleaned and standardized SKU values.
- Prepared SKU data for product matching.
- Validated the required SKU columns.
- Generated `week3_sku_prepared.csv`.
- Validated all 5,434 records.

#### 4. Fuzzy Product Matching

- Implemented fuzzy product matching using RapidFuzz.
- Compared standardized product names.
- Generated match scores and match-status information.
- Created matching group identifiers.
- Generated `week3_fuzzy_matched.csv`.
- Validated all 5,434 records.

#### 5. Gold-Ready Processing

- Processed the fuzzy-matched product data.
- Prepared the final Gold-ready dataset.
- Validated all required Gold columns.
- Verified that input and output record counts match.
- Final output contains 5,434 records.
- Generated `week3_gold_ready.csv`.
- Prepared the dataset for Silver → Gold Delta processing in Databricks.

### Week 3 Validation

| Validation | Result |
|---|---|
| Silver input records | 5,434 |
| Standardized-name records | 5,434 |
| SKU-prepared records | 5,434 |
| Fuzzy-matched records | 5,434 |
| Gold-ready records | 5,434 |
| Record-count validation | PASSED |
| Final Gold-column validation | PASSED |

### Week 3 Deliverables

- `week3_prepare_silver.py`
- `week3_standardize_names.py`
- `week3_prepare_sku.py`
- `week3_fuzzy_matching.py`
- `week3_gold_processing.py`

### Week 3 Outcome

The electronics product dataset was successfully prepared from the Silver layer into a validated Gold-ready dataset containing **5,434 records**. The dataset is ready for the next **Silver → Gold Delta processing stage in Databricks**.