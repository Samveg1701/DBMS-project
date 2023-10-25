# 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project'
import os
import csv
import psycopg2

# PostgreSQL connection information
conn = psycopg2.connect(
    dbname="postgres", user="postgres", password="asus", host="localhost"
)
conn.autocommit = True
cur = conn.cursor()

# Check if the database "flask_db" already exists
cur.execute("SELECT 1 FROM pg_database WHERE datname='flask_db'")
exists = cur.fetchone()

# If the database doesn't exist, create it
if not exists:
    cur.execute("CREATE DATABASE flask_db")
    print("flask_db database created successfully.")

# Print the name of the flask_db database
print("flask_db")

# Close the cursor and connection to the default database
cur.close()
conn.close()

# Reconnect to the "flask_db" database
conn = psycopg2.connect(
    dbname="flask_db", user="postgres", password="asus", host="localhost"
)
cur = conn.cursor()

# Directory containing the CSV files
csv_folder_path = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project'

# Iterate through the CSV files in the folder
for file_name in os.listdir(csv_folder_path):
    if file_name.endswith(".csv"):
        csv_file_path = os.path.join(csv_folder_path, file_name)

        # Read the CSV file to get column names
        with open(csv_file_path, "r", encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            headers = next(reader)

        # Modify headers to ensure the column names are valid
        headers = [header.replace(" ", "_").replace("/", "_or_") for header in headers]

        # Generate the SQL CREATE TABLE statement dynamically
        table_name = os.path.splitext(file_name)[0].replace(" ", "_")  # Use the file name as the table name
        create_table_query = f'CREATE TABLE "{table_name}" ({", ".join([f"\"{header}\" VARCHAR(255)" for header in headers])});'

        # Execute the CREATE TABLE statement
        cur.execute(create_table_query)

        # Import data from CSV file
        with open(csv_file_path, "r", encoding='utf-8-sig') as file:
            next(file)  # Skip header
            cur.copy_from(file, table_name, sep=",")

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
