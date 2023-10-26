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
from datetime import datetime

# C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project/complete.json
complete = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project/complete.json'
nation_level_daily = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project/nation_level_daily.json'
state_level_daily = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project/state_level_daily.json'
test_day_wise = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project/tests_day_wise.json'

# Read the JSON data from the file
with open(complete, 'r') as file:
    complete_json_list = json.load(file)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="DBMS", user="postgres", password="asus", host="localhost")
cur = conn.cursor()

# Iterate over the JSON objects and insert them into the table
for data in complete_json_list:
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
for data in complete_json_list:
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


# national level daily being input here
with open(nation_level_daily, 'r') as file:
    national_json_data = json.load(file)

cur.execute('''
    CREATE TABLE IF NOT EXISTS nation_level_daily (
        date VARCHAR(20),
        daily_confirmed INTEGER,
        total_confirmed INTEGER,
        daily_recovered INTEGER,
        total_recovered INTEGER,
        daily_deceased INTEGER,
        total_deceased INTEGER
    )
''')
# Insert data from each JSON object in the list into the table
for data in national_json_data:
    cur.execute("""
        INSERT INTO nation_level_daily (
            date, daily_confirmed, total_confirmed, daily_recovered, total_recovered, daily_deceased, total_deceased
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )""", (
            data['Date'],
            data['Daily Confirmed'],
            data['Total Confirmed'],
            data['Daily Recovered'],
            data['Total Recovered'],
            data['Daily Deceased'],
            data['Total Deceased']
        )
    )


# state level daily 
with open(state_level_daily, 'r') as file:
    state_level_daily_data = json.load(file)

cur.execute('''
    CREATE TABLE IF NOT EXISTS state_level_daily (
        id SERIAL PRIMARY KEY,
        field1 INTEGER,
        date DATE,
        state VARCHAR(255),
        confirmed INTEGER,
        deceased INTEGER,
        recovered INTEGER,
        state_name VARCHAR(255)
    )
''')

# Insert data from each JSON object in the list into the table
for data in state_level_daily_data:
    cur.execute("""
        INSERT INTO state_level_daily (
            field1, date, state, confirmed, deceased, recovered, state_name
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s
        )""", (
            data['FIELD1'],
            data['Date'],
            data['State'],
            data['Confirmed'],
            data['Deceased'],
            data['Recovered'],
            data['State_Name']
        )
    )

# test day wise
with open(test_day_wise, 'r') as file:
    test_day_wise_data = json.load(file)

cur.execute("DROP TABLE IF EXISTS test_day_wise")
# Create the table if it does not already exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS test_day_wise (
        update_time_stamp VARCHAR,
        tested_as_of VARCHAR,
        total_samples_tested INTEGER,
        total_individuals_tested INTEGER,
        total_positive_cases VARCHAR,
        tests_conducted_by_private_labs INTEGER,
        sample_reported_today VARCHAR(255),
        positive_cases_from_samples_reported INTEGER,
        source VARCHAR(255),
        source_1 VARCHAR(255),
        test_positivity_rate VARCHAR(255),
        individuals_tested_per_confirmed_case FLOAT,
        tests_per_confirmed_case FLOAT,
        tests_per_million INTEGER
    )
''')

# Iterate over the JSON objects and insert them into the table
for data in test_day_wise_data:
    cur.execute("""
        INSERT INTO test_day_wise (
            update_time_stamp, tested_as_of, total_samples_tested, total_individuals_tested, total_positive_cases,
            tests_conducted_by_private_labs, sample_reported_today, positive_cases_from_samples_reported, source,
            source_1, test_positivity_rate, individuals_tested_per_confirmed_case, tests_per_confirmed_case, tests_per_million
        ) VALUES (
             %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )""", (
            data['Update Time Stamp'],
            data['Tested As Of'] if data['Tested As Of'] else None,
            data['Total Samples Tested'] if data['Total Samples Tested'] else None,
            data['Total Individuals Tested'] if data['Total Individuals Tested'] else None,
            data['Total Positive Cases'] if data['Total Positive Cases'] else None,
            data['Tests conducted by Private Labs'] if data['Tests conducted by Private Labs'] else None,
            data['Sample Reported today'] if data['Sample Reported today'] != "" else None,
            data['Positive cases from samples reported'] if data['Positive cases from samples reported'] else None,
            data['Source'] if data['Source'] != "" else None,
            data['Source 1'] if data['Source 1'] != "" else None,
            data['Test positivity rate'] if data['Test positivity rate'] != "" else None,
            data['Individuals Tested Per Confirmed Case'] if data['Individuals Tested Per Confirmed Case'] else None,
            data['Tests Per Confirmed Case'] if data['Tests Per Confirmed Case'] else None,
            data['Tests per million'] if data['Tests per million'] else None
        )
    )


cur.execute("Select * from test_day_wise")
# complete_data = cur.fetchall()
state_data = cur.fetchall()

print(state_data)



# print('hey')

conn.commit()
conn.close()
# conn.commit()
# conn.close()
