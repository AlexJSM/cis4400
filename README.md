	Analysis of Afforable housing in NYC
source - https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data
# Business Requirements
- Analyze the distribution of affordable housing units across different boroughs
- Determine which income groups have the most and least access to affordable housing
# Functional Requirements
## Analyze the distribution of affordable housing units across different boroughs and neighborhoods.
- Geographic Distribution Dashboard
  	- Provide interactive maps showing the distribution of housing units across all boroughs
  	- Calculate and display density metrics of affordable housing by geographic area
- Location-Based Analytics
  	- Track and report on unit distribution patterns across different geographic levels (Borough, Community Board, Census Tract)
  	- Provide comparative analysis tools to identify areas of high and low unit concentration
  	- Generate reports on neighborhood-specific housing availability and trends
- Data Integration and Reporting
  	- Integrate with existing housing databases to maintain current information
  	- Generate automated reports on both income-based and geographic distribution metrics
  	- Provide data export capabilities for further analysis and reporting

## Determine which income groups have the most and least access to affordable housing
- Income Level Analysis System
   	- Calculate and display the total number of units available for each income category (Extremely Low, Very Low, Low, Moderate, Middle)
   	- Generate comparative reports showing the distribution of units across all income levels
- Income-Based Unit Tracking
   - Maintain a database of all housing units categorized by income eligibility
   - Provide filtering capabilities to analyze units by income level and location
   	- Generate alerts when significant disparities in unit distribution across income levels are detected


# Data Sources

### Primary Dataset
- **Source**: [NYC Open Data - Affordable Housing Production by Building](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr/about_data)
- **Contents**:
  - Project details and identifiers
  - Location information
  - Unit counts and distributions
  - Income level categorizations

### Secondary Dataset
- **Source**: [NYC Open Data - Borough Boundaries](https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm)
- **Contents**:
  - Geographic boundary data
  - Borough-specific information
  - Spatial reference data
 
  
# Information Architecture Description


### 1. Information Collection Layer
- **Source Data Structure**
  - Captures raw data from housing production and geographic datasets
  - Organizes initial data into structured categories:
    - Project Details (IDs, names, dates)
    - Location Information (boroughs, community boards)
    - Housing Units Data (counts, income levels)
  - Interacts with Data Processing Layer by providing validated input data

### 2. Information Processing Layer
- **Data Rules & Standards**
  - Defines and enforces data quality rules
  - Implements validation criteria for incoming data
  - Sets transformation rules for standardization
  - Connects with Integration Layer to ensure data consistency


### 3. Information Integration Layer
- **Unified Data Model**
  - Standardizes data formats across sources
  - Maintains common definitions
  - Creates integration mappings
  - Feeds standardized data to Storage Layer


### 4. Information Storage Layer
- **Fact Information**
  - Stores quantitative housing measures
  - Maintains relationships between facts and dimensions
  - Supports aggregation and analysis
  - Feeds data to Retrieval Layer

- **Dimensional Information**
  - Organizes descriptive attributes
  - Maintains hierarchical relationships
  - Supports drill-down capabilities
  - Provides context to fact data

### 5. Information Retrieval Layer
- **Access Layer**
  - Manages user authentication
  - Enforces security policies
  - Controls data access permissions
  - Interfaces with Presentation Layer

- **Information Presentation**
  - Generates standardized reports
  - Powers interactive dashboards
  - Provides API access
  - Delivers data visualization


# Data Architecture Description

## Data Processing Workflows

### 1. Data Extraction
- Raw data collection from NYC Open Data APIs
- Automated scheduling for regular updates
- Version control for dataset changes

### 2. Data Cleaning
- Removal of duplicates and inconsistencies
- Standardization of formats and units
- Handling of missing values
- Data quality checks

### 3. Data Transformation
- Application of business rules
- Format standardization
- Derived metrics calculation
- Geographic data processing

### 4. Data Validation
- Data completeness checks
- Business rule validation
- Geographic boundary validation
- Income level categorization verification

### Staging Area
- Temporary storage for processed data
- Pre-integration quality checks
- Version control and backup

### ETL Processes
- Automated integration workflows
- Data mapping and transformation
- Error handling and logging
- Performance optimization

### Quality Control
- Continuous monitoring
- Data quality metrics
- Alert systems for anomalies
- Audit trails

## Data Storage Solutions

### Data Warehouse
#### Fact Tables
- Housing_Units_Fact
  - Unit counts
  - Project references
  - Location references
  - Income level references

#### Dimension Tables
- Project_Dimension
  - Project details
  - Timeline information
  - Status tracking
- Location_Dimension
  - Borough information
  - Community board data
  - Census tract references
- Income_Level_Dimension
  - Income categories
  - Range definitions
  - Eligibility criteria

### Data Marts
- Project Analysis Mart
- Geographic Distribution Mart
- Income Level Analysis Mart

## Data Retrieval

### Reporting Services
- Automated report generation
- Custom report builder
- Scheduled distributions
- Export capabilities

### Analytics Platform
- Interactive dashboards
- Geographic visualization
- Trend analysis tools
- Comparative analytics

### API Services
- API endpoints
- Data access controls
- Documentation
- Rate limiting and security
