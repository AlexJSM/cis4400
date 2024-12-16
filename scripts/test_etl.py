import unittest
import pandas as pd
import os
from transform_load_data import (
    clean_data,
    transform_location_data,
    transform_project_data,
    transform_fact_data
)

class TestETLProcess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sample test data
        cls.test_data = pd.DataFrame({
            'Project ID': ['001', '002', '003'],
            'Project Name': ['Test Project 1', 'Test Project 2', 'Test Project 3'],
            'Program Group': ['Group A', 'Group B', 'Group A'],
            'Borough': ['Manhattan', 'Brooklyn', 'Queens'],
            'Community Board': ['1', '2', '3'],
            'Census Tract': ['100', '200', '300'],
            'NTA - Neighborhood Tabulation Area': ['Area1', 'Area2', 'Area3'],
            'Latitude': ['40.7128', '40.6782', '40.7282'],
            'Longitude': ['-74.0060', '-73.9442', '-73.7949'],
            'Extremely Low Income Units': ['10', '20', '30'],
            'Very Low Income Units': ['5', '15', '25'],
            'Low Income Units': ['8', '18', '28'],
            'Moderate Income Units': ['3', '13', '23'],
            'Middle Income Units': ['2', '12', '22'],
            'Total Units': ['28', '78', '128'],
            'Project Start Date': ['2023-01-01', '2023-02-01', '2023-03-01'],
            'Project Completion Date': ['2024-01-01', '2024-02-01', '2024-03-01'],
            'Project Status': ['Complete', 'In Progress', 'Planning']
        })

    def test_clean_data(self):
        # Test data cleaning
        cleaned_df = clean_data(self.test_data.copy())
        
        # Check numeric conversion
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Extremely Low Income Units']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Total Units']))
        
        # Check coordinate conversion
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Latitude']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Longitude']))

    def test_transform_location_data(self):
        # Test location dimension transformation
        location_dim = transform_location_data(self.test_data.copy())
        
        # Check expected columns
        expected_columns = [
            'Borough',
            'Community_Board',
            'Census_Tract',
            'NTA_Neighborhood',
            'Latitude',
            'Longitude'
        ]
        self.assertEqual(list(location_dim.columns), expected_columns)
        
        # Check for duplicates
        self.assertEqual(len(location_dim), len(location_dim.drop_duplicates()))

    def test_transform_project_data(self):
        # Test project dimension transformation
        project_dim = transform_project_data(self.test_data.copy())
        
        # Check expected columns
        expected_columns = [
            'Project_Key',
            'Project_Name',
            'Program_Group',
            'Project_Start_Date',
            'Project_Completion_Date',
            'Project_Status'
        ]
        self.assertEqual(list(project_dim.columns), expected_columns)
        
        # Check date conversion
        self.assertTrue(pd.api.types.is_datetime64_dtype(project_dim['Project_Start_Date']))
        self.assertTrue(pd.api.types.is_datetime64_dtype(project_dim['Project_Completion_Date']))

    def test_transform_fact_data(self):
        # Test fact table transformation
        fact_table = transform_fact_data(self.test_data.copy())
        
        # Check expected columns
        expected_columns = [
            'Project_Key',
            'Extremely_Low_Income_Units',
            'Very_Low_Income_Units',
            'Low_Income_Units',
            'Moderate_Income_Units',
            'Middle_Income_Units',
            'Total_Units'
        ]
        self.assertEqual(list(fact_table.columns), expected_columns)
        
        # Check numeric conversion
        numeric_cols = [col for col in fact_table.columns if 'Units' in col]
        for col in numeric_cols:
            self.assertTrue(pd.api.types.is_numeric_dtype(fact_table[col]))

if __name__ == '__main__':
    unittest.main()
