-- DDL Script for NYC Affordable Housing Data Warehouse
-- File: create_warehouse_tables.sql

-- Create dimension tables first
CREATE TABLE Location_Dim (
    Location_Key INT IDENTITY(1,1) PRIMARY KEY,
    Borough VARCHAR(50),
    Community_Board VARCHAR(50),
    Census_Tract VARCHAR(50),
    NTA_Neighborhood VARCHAR(255),
    Latitude DECIMAL(9,6),
    Longitude DECIMAL(9,6),
    Created_Date DATETIME DEFAULT GETDATE(),
    Modified_Date DATETIME DEFAULT GETDATE()
);

CREATE TABLE Project_Dim (
    Project_Key INT PRIMARY KEY,
    Project_Name VARCHAR(255),
    Program_Group VARCHAR(100),
    Project_Start_Date DATE,
    Project_Completion_Date DATE,
    Project_Status VARCHAR(50),
    Created_Date DATETIME DEFAULT GETDATE(),
    Modified_Date DATETIME DEFAULT GETDATE()
);

CREATE TABLE Housing_Units_Fact (
    Housing_Unit_Key INT IDENTITY(1,1) PRIMARY KEY,
    Project_Key INT FOREIGN KEY REFERENCES Project_Dim(Project_Key),
    Location_Key INT FOREIGN KEY REFERENCES Location_Dim(Location_Key),
    Extremely_Low_Income_Units INT DEFAULT 0,
    Very_Low_Income_Units INT DEFAULT 0,
    Low_Income_Units INT DEFAULT 0,
    Moderate_Income_Units INT DEFAULT 0,
    Middle_Income_Units INT DEFAULT 0,
    Total_Units INT,
    Created_Date DATETIME DEFAULT GETDATE(),
    Modified_Date DATETIME DEFAULT GETDATE()
);

-- Create indexes for better query performance
CREATE INDEX idx_project_dates ON Project_Dim(Project_Start_Date, Project_Completion_Date);
CREATE INDEX idx_location_borough ON Location_Dim(Borough);
CREATE INDEX idx_housing_units_total ON Housing_Units_Fact(Total_Units);
