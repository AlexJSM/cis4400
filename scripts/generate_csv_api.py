# API Script for generating CSV data
# File: generate_csv_api.py

from flask import Flask, send_file
import pandas as pd
import pyodbc
from io import StringIO
import csv

app = Flask(__name__)

def get_db_connection():
    '''Connect to Azure SQL Database'''
    conn_str = '''
    Driver={ODBC Driver 17 for SQL Server};
    Server=housing-sql-server.database.windows.net;
    Database=housing_db;
    UID=CloudSA09cbcc39;
    PWD=your_password_here;
    '''
    return pyodbc.connect(conn_str)

@app.route('/api/housing/units', methods=['GET'])
def get_housing_units():
    '''API endpoint to get housing units data'''
    try:
        conn = get_db_connection()
        
        query = '''
        SELECT 
            p.Project_Name,
            p.Program_Group,
            p.Project_Start_Date,
            p.Project_Completion_Date,
            l.Borough,
            l.Community_Board,
            l.NTA_Neighborhood,
            h.Extremely_Low_Income_Units,
            h.Very_Low_Income_Units,
            h.Low_Income_Units,
            h.Moderate_Income_Units,
            h.Middle_Income_Units,
            h.Total_Units
        FROM Housing_Units_Fact h
        JOIN Project_Dim p ON h.Project_Key = p.Project_Key
        JOIN Location_Dim l ON h.Location_Key = l.Location_Key
        '''
        
        df = pd.read_sql(query, conn)
        
        # Create CSV in memory
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Create response
        output = csv_buffer.getvalue()
        csv_buffer.close()
        
        return send_file(
            StringIO(output),
            mimetype='text/csv',
            as_attachment=True,
            download_name='housing_units_data.csv'
        )
        
    except Exception as e:
        return {'error': str(e)}, 500
        
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
