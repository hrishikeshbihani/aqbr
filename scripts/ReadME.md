# Data Metadata Update Scripts

This repository contains a set of scripts for managing and updating table metadata. These scripts handle the conversion of data between formats, update metadata with descriptions, and clean up XML files based on CSV input.

## Scripts Overview

### 1. `convert_metadata.py`

**Purpose:**  
Fetches table metadata from the Explorer API, converts it into XML and CSV formats, and writes these outputs to files. Also generates a CSV file with table descriptions.

**Input Files:**
- None (fetches data from the API)

**Output Files:**
- `combined_tables.xml` – XML file containing table metadata.
- `combined_tables.csv` – CSV file containing table metrics and dimensions.
- `table_descriptions.csv` – CSV file containing table names and descriptions.

### 2. `update_metric_dimensions_from_csv.py`

**Purpose:**  
Updates an XML file's metrics and dimensions sections with descriptions from a CSV file. It removes metrics and dimensions that are not present in the CSV and updates existing ones with new descriptions.

**Input Files:**
- `combined_tables.csv` – CSV file with column descriptions.
- `combined_tables.xml` – XML file to be updated.

**Output File:**
- `combined_tables.xml` – Updated XML file with descriptions and removed unused columns.

### 3. `update_table_description_from_csv.py`

**Purpose:**  
Updates or adds table descriptions in an XML file based on a CSV file. It removes tables from the XML that are not listed in the CSV.

**Input Files:**
- `table_descriptions.csv` – CSV file with updated table descriptions.
- `combined_tables.xml` – XML file to be updated.

**Output File:**
- `combined_tables.xml` – Updated XML file with new table descriptions and removed tables not present in the CSV.
