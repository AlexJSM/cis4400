# NYC Affordable Housing Analysis Project

## Project Overview
This project analyzes affordable housing production across New York City, focusing on the distribution of housing units across different income levels and geographic areas. The analysis helps identify patterns in housing development and assists in urban planning decisions.

### Business Requirements
- Track and analyze affordable housing unit distribution across NYC boroughs
- Monitor different income level categories of housing units
- Provide insights into project timelines and completion rates
- Enable geographic analysis of housing density

## Data Architecture
### Data Warehouse Implementation
- **Platform**: Azure SQL Server
- **Database**: housing_db
- **Schema**:
  - Housing_Units_Fact (Main fact table containing unit counts)
  - Location_Dim (Geographic information)
  - Project_Dim (Project details and timeline)
  - Income_Level_Dim (Income category definitions)

### Documentation
- **Data Dictionary**: Comprehensive field definitions from NYC Open Data
- **Data Mapping**: Source-to-destination mapping in NYC_Housing_Data_Mapping.xlsx
- **ETL Documentation**: Python-based transformation processes

## Technical Implementation
### Technologies Used
- **Database**: Azure SQL Server
- **ETL Process**: Python scripts for data transformation
- **Visualization**: 
  - Tableau Public for interactive dashboards
  - AWS QuickSight for cloud-based analytics

### Data Processing Workflow
1. Data extraction from NYC Open Data
2. Transformation using Python scripts
3. Loading into Azure SQL Server
4. Integration with visualization tools

## Visualizations
### Tableau Dashboard
- **Live Dashboard**: [NYC Affordable Housing Analysis Dashboard](https://public.tableau.com/app/profile/alex.santana2165/viz/CIS4400HW2VIZUALS/Dashboard1?publish=yes)
- **Features**:
  - Geographic Distribution Map
  - Income Level Distribution
  - Project Timeline Analysis
  - Unit Type Comparison
  - Borough-wise Analysis
## Visualizations

The following visualizations have been created to analyze the NYC Affordable Housing data:

### 1. Income Level Distribution
- A pie chart showing the distribution of housing units across different income levels.
<img src="snapshots/Income Level Distribution.png" alt="Income Level Distribution" width="800"/>

### 2. Geographic Distribution Map
- A map visualizing the geographic distribution of housing units across NYC boroughs.
<img src="snapshots/Geographic Distribution Map.png" alt="Geographic Distribution Map" width="800"/>

### 3. Heat Map Based on Community Board Section
- A heat map highlighting housing density by community board sections.
<img src="snapshots/Heat Map based on Community Board Section.png" alt="Heat Map Based on Community Board Section" width="800"/>

### 4. Time-based Project Analysis
- A line chart analyzing project timelines and completion rates.
<img src="snapshots/Time-based Project Analysis.png" alt="Time-based Project Analysis" width="800"/>

### 5. Income Category Number of Units by Borough
- A column chart comparing the number of units by income category across boroughs.
<img src="snapshots/Income Category Number of Units by Borough.png" alt="Income Category Number of Units by Borough" width="800"/>


## Setup and Usage
### 1. Database Connection
```
Server: housing-sql-server.database.windows.net
Database: housing_db

```

## Data Sources
### Primary Source
- [NYC Open Data Portal](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data)
- Department of Housing Preservation and Development (HPD)
- Dataset: Affordable Housing Production by Building
