import sqlite3

import keyring

# Path to the SQLite database
sqlite_db_path = 'F:/job_search_utilities/Data/secrets/super_secret_database.sqlite'

# Connect to the SQLite database
conn = sqlite3.connect(sqlite_db_path)
cursor = conn.cursor()

# Select all data from the table
cursor.execute("SELECT * FROM password_table")
rows = cursor.fetchall()

# Column indexes (assuming the order is login_url, username, password)
LOGIN_URL = 1
USERNAME = 2
PASSWORD = 3

for row in rows:
    login_url, username, password = row[LOGIN_URL], row[USERNAME], row[PASSWORD]

    # Retrieve the existing password from the keyring
    stored_password = keyring.get_password(login_url, username)

    if stored_password is None or stored_password != password:
        # If the service does not exist, create new entry in keyring
        keyring.set_password(login_url, username, password)

# Verification pass
for row in rows:
    login_url, username, password = row[LOGIN_URL], row[USERNAME], row[PASSWORD]
    stored_password = keyring.get_password(login_url, username)

    if stored_password != password:
        print(f"Verification failed for {login_url} with username {username}")
    else:
        print(f"Verification passed for {login_url} with username {username}")

# Close the database connection
conn.close()
