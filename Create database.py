# # # 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project'
# # import os
# # import csv
# # import psycopg2
# # import json
# # import time

# # # PostgreSQL connection information
# # conn = psycopg2.connect(
# #     dbname="postgres", user="postgres", password="asus", host="localhost"
# # )
# # conn.autocommit = True
# # cur = conn.cursor()

# # # Check if the database "flask_db" already exists
# # cur.execute("SELECT 1 FROM pg_database WHERE datname='flask_db'")
# # exists = cur.fetchone()

# # # If the database doesn't exist, create it
# # if not exists:
# #     cur.execute("CREATE DATABASE flask_db")
# #     print("flask_db database created successfully.")

# # # Print the name of the flask_db database
# # print("flask_db")

# # # Close the cursor and connection to the default database
# # cur.close()
# # conn.close()

# # # Reconnect to the "flask_db" database
# # conn = psycopg2.connect(
# #     dbname="flask_db", user="postgres", password="asus", host="localhost"
# # )
# # cur = conn.cursor()

# # # Directory containing the CSV files
# # csv_folder_path = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project'

# # # Iterate through the CSV files in the folder
# # for file_name in os.listdir(csv_folder_path):
# #     if file_name.endswith(".csv"):
# #         csv_file_path = os.path.join(csv_folder_path, file_name)

# #         # Read the CSV file to get column names
# #         with open(csv_file_path, "r", encoding='utf-8-sig') as file:
# #             reader = csv.reader(file)
# #             headers = next(reader)

# #         # Modify headers to ensure the column names are valid
# #         headers = [header.replace(" ", "_").replace("/", "_or_") for header in headers]

# #         # Generate the SQL CREATE TABLE statement dynamically
# #         table_name = os.path.splitext(file_name)[0].replace(" ", "_")  # Use the file name as the table name
# #         columns = [f'"{header}" VARCHAR(255)' for header in headers]
# #         create_table_query = f'CREATE TABLE "{table_name}" ({", ".join(columns)});'

# #         # Execute the CREATE TABLE statement
# #         cur.execute(create_table_query)

# #         # Import data from CSV file
# #         with open(csv_file_path, "r", encoding='utf-8-sig') as file:
# #             next(file)  # Skip header
# #             cur.copy_from(file, table_name, sep=",")

# # # Commit the changes
# # conn.commit()

# # # Close the cursor and connection
# # cur.close()
# # conn.close()


# # dataset = 'C:/Users/asus/Downloads/complete.json'
# # def start_database():  # Create table and fill it
# #     cur.execute(
# #                 "CREATE TABLE IF NOT EXISTS Complete (Date DATE, State VARCHAR(30), Latitude VARCHAR(10), Longitude VARCHAR(10), deaths INT, country VARCHAR(100), geoId VARCHAR(15), popData2018 BIGINT, continent VARCHAR(50), PRIMARY KEY (fulldate, country))")
# #     # fill_database()


# # with open(dataset) as json_file:

# #         data = json.load(json_file)

# #         dataset_rows = 0
# #         rows_inserted = 1
# #         for p in data['records']:
# #             dataset_rows += 1  # Count the items/records (json objects) of the dataset

# #         print('This might take a while the first time...')
# #         start = time.time()
# #         for p in data['records']:  # For each item in the dataset

# #             print(f'\rInserting to database: {rows_inserted} / {dataset_rows} rows', end="", flush=True)

# #             # date = p['Date'][6:10] + '-' + p['Date'][3:5] + '-' + p['Date'][0:2]  # Convert date from dd/mm/yyyy to yyyy-mm-dd
# #             if p['popData2019']:  # If there are population data for the current country
# #                 sql = f"INSERT IGNORE INTO CountriesPerDay VALUES ('{p['year']}', '{p['month']}', '{p['day']}', '{date}', {p['cases']}, {p['deaths']}, '{p['countriesAndTerritories']}', '{p['geoId']}', {p['popData2019']}, '{p['continentExp']}' )"
# #             else:  # Insert NULL on 'popData2018'
# #                 sql = f"INSERT IGNORE INTO CountriesPerDay VALUES ('{p['year']}', '{p['month']}', '{p['day']}', '{date}', {p['cases']}, {p['deaths']}, '{p['countriesAndTerritories']}', '{p['geoId']}', NULL, '{p['continentExp']}' )"
# #             sql = f"INSERT INTO "
# #             mycursor.execute(sql)

# #             mydb.commit()

# #             rows_inserted += 1

# #         end = time.time() - start
# #         print('\n\nTime taken: ' + '{:.2f} seconds'.format(end))
# #         print('\n')




# from flask import Flask
# import psycopg2

# app = Flask(__name__)

# # Configure the PostgreSQL connection
# def connect_db():
#     conn = psycopg2.connect(
#     dbname="DBMS", user="postgres", password="asus", host="localhost")
#     return conn.cursor

# # Sample route to test the connection
# cur = connect_db()
# cur.execute("Select * from complete")
# records = cur.fetchall()

# if __name__ == '__main__':
#     app.run(debug=True)


import psycopg2
import json

dataset = 'C:/Users/asus/Downloads/complete.json'

# Read the JSON data from the file
with open(dataset, 'r') as file:
    json_list = json.load(file)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="DBMS", user="postgres", password="asus", host="localhost")
cur = conn.cursor()

# Iterate over the JSON objects and insert them into the table
for data in json_list:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS covid_data (
        id SERIAL PRIMARY KEY,
        date DATE,
        state VARCHAR(255),
        latitude FLOAT,
        longitude FLOAT,
        total_confirmed_cases INTEGER,
        death INTEGER,
        discharged_migrated INTEGER,
        new_cases INTEGER,
        new_deaths INTEGER,
        new_recovered INTEGER
    )
''')

# Insert data from each JSON object in the list into the table
for data in json_list:
    records = cur.execute("""
        INSERT INTO covid_data (
            date, state, latitude, longitude, total_confirmed_cases, death, discharged_migrated, new_cases, new_deaths, new_recovered
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""", (
            data['Date'],
            data['Name of State '][' UT'],
            float(data['Latitude']),
            float(data['Longitude']),
            int(data['Total Confirmed cases']),
            str(data['Death']),
            int(data['Cured']['Discharged']['Migrated']),
            int(data['New cases']),
            int(data['New deaths']),
            int(data['New recovered'])
        )
    )
cur.execute("Select * from covid_data")
records2 = cur.fetchall()
print(records2)

conn.commit()
conn.close()
# conn.commit()
# conn.close()
