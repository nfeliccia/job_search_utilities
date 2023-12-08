import sqlite3

import pandas as pd

# Path to the Excel file
excel_file_path = 'F:/job_search_utilities/Data/secrets/password_seed.xlsx'

# Read the Excel file
df = pd.read_excel(excel_file_path, sheet_name='Sheet1')

# Convert all columns to string type
df = df.astype(str)

# Path to the SQLite database
sqlite_db_path = 'F:/job_search_utilities/Data/secrets/super_secret_database.sqlite'

# Create a connection to the SQLite database
conn = sqlite3.connect(sqlite_db_path)

# Create a cursor object using the cursor method
cursor = conn.cursor()

# Create a table named 'password_table'
# Generate the column definitions based on the DataFrame columns
columns = ', '.join([f'"{col}" TEXT' for col in df.columns])
create_table_query = f'CREATE TABLE IF NOT EXISTS password_table ({columns})'
cursor.execute(create_table_query)

# Insert data from the DataFrame into the SQLite table
df.to_sql('password_table', conn, if_exists='append', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()
