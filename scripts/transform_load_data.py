# ETL Script for NYC Affordable Housing Data
# File: transform_load_data.py

import pandas as pd
import pyodbc
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
import os
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl.log'),
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

def connect_to_db():
    '''Connect to Azure SQL Database'''
    try:
        conn_str = f'''
        Driver={{ODBC Driver 17 for SQL Server}};
        Server={os.getenv('DB_SERVER')};
        Database={os.getenv('DB_NAME')};
        UID={os.getenv('DB_USERNAME')};
        PWD={os.getenv('DB_PASSWORD')};
        '''
        return pyodbc.connect(conn_str)
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        raise

def load_source_data():
    '''Load data from NYC Open Data'''
    try:
        url = "https://data.cityofnewyork.us/api/views/hg8x-zxpr/rows.csv"
        logging.info("Loading data from NYC Open Data...")
        df = pd.read_csv(url)
        logging.info(f"Loaded {len(df)} rows of data")
        return df
    except Exception as e:
        logging.error(f"Error loading source data: {str(e)}")
        raise

def clean_data(df):
    '''Clean and prepare the data'''
    try:
        # Remove any leading/trailing whitespace
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()

        # Convert numeric columns
        numeric_columns = [
            'Extremely Low Income Units',
            'Very Low Income Units',
            'Low Income Units',
            'Moderate Income Units',
            'Middle Income Units',
            'Total Units'
        ]
        
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Convert coordinates to numeric
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

        return df
    except Exception as e:
        logging.error(f"Error cleaning data: {str(e)}")
        raise

def transform_location_data(df):
    '''Transform and prepare location dimension data'''
    try:
        location_df = df[[
            'Borough',
            'Community Board',
            'Census Tract',
            'NTA - Neighborhood Tabulation Area',
            'Latitude',
            'Longitude'
        ]].drop_duplicates()

        location_df.columns = [
            'Borough',
            'Community_Board',
            'Census_Tract',
            'NTA_Neighborhood',
            'Latitude',
            'Longitude'
        ]

        # Remove rows with all NULL values
        location_df = location_df.dropna(how='all')

        return location_df
    except Exception as e:
        logging.error(f"Error transforming location data: {str(e)}")
        raise

def transform_project_data(df):
    '''Transform and prepare project dimension data'''
    try:
        project_df = df[[
            'Project ID',
            'Project Name',
            'Program Group',
            'Project Start Date',
            'Project Completion Date',
            'Project Status'
        ]].drop_duplicates()

        project_df.columns = [
            'Project_Key',
            'Project_Name',
            'Program_Group',
            'Project_Start_Date',
            'Project_Completion_Date',
            'Project_Status'
        ]

        # Convert dates
        for date_col in ['Project_Start_Date', 'Project_Completion_Date']:
            project_df[date_col] = pd.to_datetime(
                project_df[date_col],
                errors='coerce'
            )

        return project_df
    except Exception as e:
        logging.error(f"Error transforming project data: {str(e)}")
        raise

def transform_fact_data(df):
    '''Transform and prepare fact table data'''
    try:
        fact_columns = {
            'Project ID': 'Project_Key',
            'Extremely Low Income Units': 'Extremely_Low_Income_Units',
            'Very Low Income Units': 'Very_Low_Income_Units',
            'Low Income Units': 'Low_Income_Units',
            'Moderate Income Units': 'Moderate_Income_Units',
            'Middle Income Units': 'Middle_Income_Units',
            'Total Units': 'Total_Units'
        }

        fact_df = df[list(fact_columns.keys())].copy()
        fact_df = fact_df.rename(columns=fact_columns)

        # Convert numeric columns
        numeric_cols = [col for col in fact_df.columns if 'Units' in col]
        for col in numeric_cols:
            fact_df[col] = pd.to_numeric(fact_df[col], errors='coerce').fillna(0)

        return fact_df
    except Exception as e:
        logging.error(f"Error transforming fact data: {str(e)}")
        raise

def load_dimension_tables(conn, location_dim, project_dim):
    '''Load dimension tables into the database'''
    try:
        cursor = conn.cursor()
        
        # Load Location dimension
        logging.info("Loading Location dimension table...")
        for _, row in tqdm(location_dim.iterrows(), total=len(location_dim)):
            cursor.execute('''
                INSERT INTO Location_Dim (
                    Borough,
                    Community_Board,
                    Census_Tract,
                    NTA_Neighborhood,
                    Latitude,
                    Longitude
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['Borough'],
                row['Community_Board'],
                row['Census_Tract'],
                row['NTA_Neighborhood'],
                row['Latitude'],
                row['Longitude']
            ))

        # Load Project dimension
        logging.info("Loading Project dimension table...")
        for _, row in tqdm(project_dim.iterrows(), total=len(project_dim)):
            cursor.execute('''
                INSERT INTO Project_Dim (
                    Project_Key,
                    Project_Name,
                    Program_Group,
                    Project_Start_Date,
                    Project_Completion_Date,
                    Project_Status
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['Project_Key'],
                row['Project_Name'],
                row['Program_Group'],
                row['Project_Start_Date'],
                row['Project_Completion_Date'],
                row['Project_Status']
            ))

        conn.commit()
        logging.info("Dimension tables loaded successfully")
    except Exception as e:
        logging.error(f"Error loading dimension tables: {str(e)}")
        conn.rollback()
        raise

def load_fact_table(conn, fact_df):
    '''Load fact table into the database'''
    try:
        cursor = conn.cursor()
        
        logging.info("Loading Housing Units fact table...")
        for _, row in tqdm(fact_df.iterrows(), total=len(fact_df)):
            cursor.execute('''
                INSERT INTO Housing_Units_Fact (
                    Project_Key,
                    Extremely_Low_Income_Units,
                    Very_Low_Income_Units,
                    Low_Income_Units,
                    Moderate_Income_Units,
                    Middle_Income_Units,
                    Total_Units
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['Project_Key'],
                row['Extremely_Low_Income_Units'],
                row['Very_Low_Income_Units'],
                row['Low_Income_Units'],
                row['Moderate_Income_Units'],
                row['Middle_Income_Units'],
                row['Total_Units']
            ))

        conn.commit()
        logging.info("Fact table loaded successfully")
    except Exception as e:
        logging.error(f"Error loading fact table: {str(e)}")
        conn.rollback()
        raise

def validate_data(conn):
    '''Validate the loaded data'''
    try:
        cursor = conn.cursor()
        
        # Check row counts
        cursor.execute("SELECT COUNT(*) FROM Location_Dim")
        location_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Project_Dim")
        project_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Housing_Units_Fact")
        fact_count = cursor.fetchone()[0]
        
        logging.info(f"Validation Results:")
        logging.info(f"Location_Dim rows: {location_count}")
        logging.info(f"Project_Dim rows: {project_count}")
        logging.info(f"Housing_Units_Fact rows: {fact_count}")
        
        # Check for orphaned records
        cursor.execute('''
            SELECT COUNT(*) 
            FROM Housing_Units_Fact f 
            LEFT JOIN Project_Dim p ON f.Project_Key = p.Project_Key 
            WHERE p.Project_Key IS NULL
        ''')
        orphaned_projects = cursor.fetchone()[0]
        
        if orphaned_projects > 0:
            logging.warning(f"Found {orphaned_projects} orphaned records in fact table")
        else:
            logging.info("No orphaned records found")
            
    except Exception as e:
        logging.error(f"Error validating data: {str(e)}")
        raise

def main():
    '''Main ETL process'''
    conn = None
    try:
        # Load source data
        source_df = load_source_data()
        
        # Clean the data
        cleaned_df = clean_data(source_df)
        
        # Transform dimension and fact data
        location_dim = transform_location_data(cleaned_df)
        project_dim = transform_project_data(cleaned_df)
        fact_table = transform_fact_data(cleaned_df)
        
        # Connect to database
        conn = connect_to_db()
        
        # Load dimension tables
        load_dimension_tables(conn, location_dim, project_dim)
        
        # Load fact table
        load_fact_table(conn, fact_table)
        
        # Validate the loaded data
        validate_data(conn)
        
        logging.info("ETL process completed successfully!")
        
    except Exception as e:
        logging.error(f"ETL process failed: {str(e)}")
        if conn:
            conn.rollback()
        raise
        
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed")

if __name__ == "__main__":
    main()
