# EchoChain – Circular Economy & Secondary Market Lifecycle Analytics

## Project Overview

EchoChain is a Circular Economy and Secondary Market Lifecycle Analytics project focused on analyzing secondary-market electronic products.

The project uses a data engineering and analytics pipeline to ingest, process, transform, and visualize secondary-market data.

---

# My Role

**Name:** V. Mohammed Ibad  
**Role:** Databricks & Delta Lake Engineer

My responsibility in the project is focused on the Databricks and Delta Lake data engineering layer.

### Responsibilities

- Set up the Databricks workspace
- Prepare the environment for the data pipeline
- Initialize Delta Lake storage
- Ingest secondary-market product data
- Create and manage the Bronze Layer
- Validate ingested data
- Prepare data for the next transformation stage

---

# Week 1 – Databricks & Delta Lake

## Databricks Workspace Setup

The Databricks environment was prepared for the EchoChain data pipeline.

The environment provides the foundation for storing and processing secondary-market product data using Delta Lake.

---

## Data Preparation

The mock secondary-market product data was prepared for ingestion into Databricks.

The dataset contains product listing information such as:

- Product ID
- Price availability
- Product condition
- Currency
- Price/date information
- Other product listing attributes

The data was loaded into the Databricks environment for further processing.

---

# Bronze Layer

The Bronze Layer was created in Databricks using Delta Lake.

The ingested secondary-market product data was written into a Delta table.

### Purpose of the Bronze Layer

- Store the ingested source data
- Preserve the original data structure
- Provide a reliable starting point for further transformation
- Maintain the raw data before downstream processing

---

# Bronze Data Validation

The Bronze Delta table was validated after ingestion.

### Validation Activities

- Checked the loaded records
- Reviewed the table structure
- Checked the available columns
- Checked the data displayed in Databricks
- Verified that the Bronze table was successfully created

The Bronze data is ready for the next stage of the EchoChain data pipeline.

---

# Week 1 Deliverables

- Databricks workspace setup
- Delta Lake environment preparation
- Secondary-market data preparation
- Bronze Delta table
- Bronze data validation
- Verified ingested data

---

# Data Pipeline

```text
Secondary-Market Data
        │
        ▼
   Databricks
        │
        ▼
   Delta Lake
        │
        ▼
 Bronze Layer
        │
        ▼
Data Transformation
        │
        ▼
 Silver Layer
        │
        ▼
 Gold / Analytics Layer- Initialize Delta Lake storage
- Ingest secondary-market product data
- Create and manage the Bronze Layer
- Validate ingested data
- Prepare data for the next transformation stage

---

# Week 1 – Databricks & Delta Lake

## Databricks Workspace Setup

The Databricks environment was prepared for the EchoChain data pipeline.

The environment provides the foundation for storing and processing secondary-market product data using Delta Lake.

---

## Data Preparation

The mock secondary-market product data was prepared for ingestion into Databricks.

The dataset contains product listing information such as:

- Product ID
- Price availability
- Product condition
- Currency
- Price/date information
- Other product listing attributes

The data was loaded into the Databricks environment for further processing.

---

# Bronze Layer

The Bronze Layer was created in Databricks using Delta Lake.

The ingested secondary-market product data was written into a Delta table.

### Purpose of the Bronze Layer

- Store the ingested source data
- Preserve the original data structure
- Provide a reliable starting point for further transformation
- Maintain the raw data before downstream processing

---

# Bronze Data Validation

The Bronze Delta table was validated after ingestion.

### Validation Activities

- Checked the loaded records
- Reviewed the table structure
- Checked the available columns
- Checked the data displayed in Databricks
- Verified that the Bronze table was successfully created

The Bronze data is ready for the next stage of the EchoChain data pipeline.

---

# Week 1 Deliverables

- Databricks workspace setup
- Delta Lake environment preparation
- Secondary-market data preparation
- Bronze Delta table
- Bronze data validation
- Verified ingested data

---

# Data Pipeline

```text
Secondary-Market Data
        │
        ▼
   Databricks
        │
        ▼
   Delta Lake
        │
        ▼
 Bronze Layer
        │
        ▼
Data Transformation
        │
        ▼
 Silver Layer
        │
        ▼
 Gold / Analytics Layer


# Week 2 – Lakehouse Ingestion & Silver Layer

## Lakehouse Ingestion

During Week 2, the EchoChain pipeline continued from the Bronze Layer toward the Silver Layer.

The secondary-market product data was processed for the next stage of the lakehouse architecture.

The existing project dataset was used for the transformation and validation process.

---

## Silver Layer Transformation

The Silver Layer was prepared from the processed secondary-market product data.

The data transformation included:

- Data cleaning
- Handling missing values
- Text cleaning
- Price validation
- Duplicate validation
- SKU extraction
- Data standardization

The transformed output was provided as a Parquet dataset for use in Databricks.

---

## Silver Data in Databricks

The Silver Parquet output was loaded into Databricks.

A Silver table was created:

workspace.default.silver_electronics_products

The table contains *5,434 records* after the transformation process.

---

## Silver Data Validation

The Silver table was validated using SQL in Databricks.

### Validation Activities

- Checked the total number of records
- Checked missing IDs
- Checked missing product names
- Checked missing prices
- Checked missing SKUs
- Checked negative prices
- Checked repeated product IDs
- Checked exact duplicate rows
- Reviewed the Silver table structure

### Validation Results

- *Total Records:* 5,434
- *Missing IDs:* 0
- *Missing Names:* 0
- *Missing Prices:* 0
- *Missing SKUs:* 0
- *Negative Prices:* 0
- *Exact Duplicate Rows:* 0

Repeated product IDs were reviewed and found to represent different historical records rather than exact duplicate rows.

---

# Week 2 Deliverables

- Lakehouse ingestion progress
- Silver Parquet dataset
- Silver table in Databricks
- silver_electronics_products Delta/Databricks table
- Silver data validation
- Data-quality validation results
- Verified 5,434 Silver records

---

# Week 2 Data Pipeline

```text
Secondary-Market Data
        │
        ▼
   Databricks
        │
        ▼
   Delta Lake
        │
        ▼
 Bronze Layer
        │
        ▼
PySpark Transformation
        │
        ▼
 Silver Parquet
        │
        ▼
Silver Table
        │
        ▼
Data Validation
        │
        ▼
Ready for Week 3
