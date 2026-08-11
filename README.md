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
 Gold / Analytics Layer
