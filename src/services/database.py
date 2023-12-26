import csv
import sqlite3
import shutil
import os
import filecmp
from paths import ROOT_DIR, PROPERTY_DIR

csv_file_path = PROPERTY_DIR / 'data.csv'
db_name = ROOT_DIR / 'elements_data.db' 

def create_database():
    # Check if the database file already exists
    if os.path.exists(db_name):
        # If the database exists, create a temporary database
        temp_db_name = ROOT_DIR / 'temp_elements_data.db'

        conn_temp = sqlite3.connect(temp_db_name)
        cursor_temp = conn_temp.cursor()

        # Create the same table in the temporary database
        cursor_temp.execute('''
            CREATE TABLE IF NOT EXISTS elements (
                atomic_number INTEGER PRIMARY KEY,
                full_name TEXT,
                symbol TEXT,
                atomic_weight REAL,
                category TEXT,
                property1 TEXT,
                property2 TEXT,
                property3 TEXT
                -- Add more properties as needed
            )
        ''')

        # Read data from the CSV file and insert into the temporary table
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    cursor_temp.execute("INSERT INTO elements VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                       (row['atomic_number'], row['full_name'], row['symbol'],
                                        row['atomic_weight'], row['category'], row['property 1'],
                                        row['property 2'], row['property 3']))
                except sqlite3.IntegrityError as e:
                    pass
                    # print(f"Error inserting row with atomic_number {row['atomic_number']}: {e}")

        conn_temp.commit()
        conn_temp.close()

        # Compare the existing and temporary databases
        if not filecmp.cmp(db_name, temp_db_name):
            # If different, replace the existing database with the temporary one
            os.remove(db_name)
            shutil.move(temp_db_name, db_name)
            # print(f"Database '{db_name}' replaced with data from '{csv_file_path}'.")
        else:
            # If the same, remove the temporary database
            os.remove(temp_db_name)
            # print(f"No changes detected. Existing database '{db_name}' is unchanged.")
    else:
        # If the database does not exist, create a new one
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create a table with columns based on CSV headers
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS elements (
                atomic_number INTEGER PRIMARY KEY,
                full_name TEXT,
                symbol TEXT,
                atomic_weight REAL,
                category TEXT,
                property1 TEXT,
                property2 TEXT,
                property3 TEXT
                -- Add more properties as needed
            )
        ''')

        # Read data from the CSV file and insert into the table
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                cursor.execute("INSERT INTO elements VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                               (row['atomic_number'], row['full_name'], row['symbol'],
                                row['atomic_weight'], row['category'], row['property 1'],
                                row['property 2'], row['property 3']))

        conn.commit()
        conn.close()

        # print(f"New database '{db_name}' created and populated with data from '{csv_file_path}'.")

def retrieve_data(row=None, column_names=None):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    if column_names is None:
        cursor.execute("SELECT * FROM elements")
    else:
        columns_str = ', '.join(column_names)
        cursor.execute(f"SELECT {columns_str} FROM elements")

    rows = cursor.fetchall()
    conn.close()

    if row is not None:
        return rows[row-1]
    else:
        return rows

    
def get_database_size():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM elements")
    count = cursor.fetchone()[0]
    conn.close()

    return count