# NYC Affordable Housing Data ETL Project

## Overview
This project focuses on extracting, transforming, and loading (ETL) NYC affordable housing data into a structured data warehouse for analysis. The repository includes scripts for data processing, table creation, and validation.

## Scripts Overview
- **create_warehouse_tables.sql**: SQL script to create tables in the data warehouse.
- **generate_csv_api.py**: Python script to fetch data from an API and save it as CSV files.
- **transform_load_data.py**: Python script to transform and load data into the data warehouse.

## How to Run the Scripts
1. **create_warehouse_tables.sql**:
   - Run this script in your SQL database to create the necessary tables.

2. **generate_csv_api.py**:
   - Execute the script using Python to fetch data from the API and save it as CSV files.
   - Command: `python generate_csv_api.py`

3. **transform_load_data.py**:
   - Execute the script using Python to perform the ETL process.
   - Command: `python transform_load_data.py`

## Data Validation
- **Input Validation**: Ensure all required fields are present in the source data.
- **Transformation Validation**: Verify that data transformations meet business rules.
- **Output Validation**: Confirm that data is correctly loaded into the target database.

## Testing
### Test Cases for ETL Process
1. **Test Data Transformation**:
   - Validate that numeric fields are correctly converted and missing values are handled.
   - Example: Check that `Extremely Low Income Units` is converted to numeric and nulls are replaced with 0.

2. **Test Data Loading**:
   - Verify that data is inserted into the database without errors.
   - Example: Check row counts in the `Housing_Units_Fact` table after loading.

3. **Test Error Handling**:
   - Simulate missing or invalid data and ensure the script logs appropriate error messages.

## Environment Setup
- Install required Python packages: `pip install -r requirements.txt`
- Set up environment variables in a `.env` file:
  ```
  DB_SERVER=<your_database_server>
  DB_NAME=<your_database_name>
  DB_USERNAME=<your_username>
  DB_PASSWORD=<your_password>
  ```

## Logs
- Logs are saved in `etl.log` for debugging and monitoring.

## Contributors
- [Your Name]

