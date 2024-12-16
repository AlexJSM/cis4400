# Data Validation Documentation

## Overview
This document outlines the data validation steps and checks performed during the ETL process for the NYC Affordable Housing Data project.

## Input Data Validation

### Required Fields
- Project ID
- Project Name
- Program Group
- Borough
- Community Board
- Census Tract
- NTA - Neighborhood Tabulation Area
- Latitude/Longitude
- Income Units (all categories)
- Project Dates
- Project Status

### Data Type Validation
1. Numeric Fields:
   - All Income Units fields
   - Latitude/Longitude coordinates
   
2. Date Fields:
   - Project Start Date
   - Project Completion Date

3. Text Fields:
   - Project ID
   - Project Name
   - Borough
   - Program Group
   - Project Status

## Transformation Validation

### Location Dimension
- Verify unique combinations of location attributes
- Ensure valid coordinate ranges
- Check for missing or invalid borough names

### Project Dimension
- Verify unique Project IDs
- Validate date ranges
- Check for valid project status values

### Fact Table
- Ensure all units are non-negative
- Verify Total Units matches sum of individual unit categories
- Check for orphaned records

## Output Validation

### Database Checks
1. Row Count Validation:
   - Compare source and target record counts
   - Verify dimension table relationships

2. Data Quality Checks:
   - Check for null values in required fields
   - Verify referential integrity
   - Validate aggregated totals

### Error Handling
- Log validation failures
- Track rejected records
- Document data quality issues

## Monitoring and Reporting
- Generate validation summary reports
- Track validation metrics over time
- Alert on validation failures
