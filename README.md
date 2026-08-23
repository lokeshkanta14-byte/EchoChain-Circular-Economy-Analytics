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
