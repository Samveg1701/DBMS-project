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
covid19africa = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_africa.json'
covid19asia = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_asia.json'
covid19europe = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_europe.json'
covid19northamerica = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_northamerica.json'
covid19ocenia = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_oceania.json'
covid19southamerica = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_southamerica.json'
covid19tests = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_tests.json'
covid19world = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_world.json'
worldpopulation = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/World_population(2020).json'
# C:\Users\asus\OneDrive\Desktop\University\Semester 7\DBMS\New dataset\World_population(2020).json

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="DBMS", user="postgres", password="asus", host="localhost")
cur = conn.cursor()

# Read the JSON data from the file
with open(covid19africa, 'r') as file:
    covid19_africa = json.load(file)

# test day wise
with open(covid19asia, 'r') as file:
    covid19_asia = json.load(file)

with open(covid19europe, 'r') as file:
    covid19_europe = json.load(file)

with open(covid19northamerica, 'r') as file:
    covid19_northamerica = json.load(file)

with open(covid19ocenia, 'r') as file:
    covid19_ocenia = json.load(file)

with open(covid19southamerica, 'r') as file:
    covid19_southamerica = json.load(file)

# with open(covid19tests, 'r') as file:
#     covid19_tests = json.load(file)

with open(covid19world, 'r') as file:
    covid19_world = json.load(file)

with open(worldpopulation, 'r') as file:
    world_population = json.load(file)


def insert_json_data_to_postgres(json_data, table_name, cur):
    # Drop the table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create a new table
    cur.execute(f'''
        CREATE TABLE {table_name} (
            observation_date DATE,
            country VARCHAR(255),
            region VARCHAR(255),
            confirmed INTEGER,
            deaths INTEGER,
            recovered INTEGER,
            active INTEGER
        )
    ''')

    # Insert data into the table
    for data in json_data:
        if isinstance(data, dict) and all(key in data for key in ['ObservationDate', 'Country', 'Region', 'Confirmed', 'Deaths', 'Recovered', 'Active']):
            observation_date = datetime.strptime(data["ObservationDate"], '%Y-%m-%d').date()
            cur.execute(f"""
                INSERT INTO {table_name} (
                    observation_date, country, region, confirmed, deaths, recovered, active
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )""", (
                    observation_date,
                    data["Country"],
                    data["Region"],
                    data["Confirmed"],
                    data["Deaths"],
                    data["Recovered"],
                    data["Active"]
                )
            )


def create_table_from_json(json_data, table_name, cur):
    # Drop the table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create a new table
    cur.execute(f'''
        CREATE TABLE {table_name} (

            country VARCHAR(255),
            population INTEGER,
            yearly_change VARCHAR(255),
            net_change INTEGER,
            density_km2 INTEGER,
            land_area_km2 INTEGER,
            migrants_net INTEGER,
            fertility_rate VARCHAR(255),
            median_age VARCHAR(255),
            urban_population_percent VARCHAR(255),
            world_share VARCHAR(255)
        )
    ''')

    # Insert data into the table
    for data in json_data:
        cur.execute("""
            INSERT INTO {} (
                country, population, yearly_change, net_change, density_km2, land_area_km2,
                migrants_net, fertility_rate, median_age, urban_population_percent, world_share
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""".format(table_name), (
                data['Country (or dependency)'],
                data['Population (2020)'],
                data['Yearly Change'],
                data['Net Change'],
                data['Density (P']['Km²)'],
                data['Land Area (Km²)'],
                data['Migrants (net)'],
                data['Fert. Rate'],
                data['Med. Age'],
                data['Urban Pop %'],
                data['World Share']
            )
        )

def create_test_table_from_json(json_data, table_name, cur):
    # Drop the table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create a new table
    cur.execute(f'''
        CREATE TABLE {table_name} (
            id SERIAL PRIMARY KEY,
            date DATE,
            country_other VARCHAR(255),
            total_tests VARCHAR(255),
            population VARCHAR(255),
            tests_per_1m_pop VARCHAR(255),
            one_test_every_x_people VARCHAR(255)
        )
    ''')

    # Insert data into the table
    for data in json_data:
        cur.execute("""
            INSERT INTO {} (
                date, country_other, total_tests, population, tests_per_1m_pop, one_test_every_x_people
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )""".format(table_name), (
                data['Date'],
                data['Country,Other'],
                data['TotalTests'],
                data['Population'],
                data['Tests']['1M pop'],
                data.get('1 Testevery X ppl', None)
            )
        )

# Call the function with the JSON data, table name, and cursor
insert_json_data_to_postgres(covid19africa, "covid19africa", cur)
insert_json_data_to_postgres(covid19asia, 'covid19_asia', cur)
insert_json_data_to_postgres(covid19europe, 'covid19_europe', cur)
insert_json_data_to_postgres(covid19northamerica, 'covid19_northamerica', cur)
insert_json_data_to_postgres(covid19southamerica, 'covid19_southamerica', cur)
insert_json_data_to_postgres(covid19world, 'covid19_world', cur)
create_table_from_json(worldpopulation, 'world_population', cur)
# create_test_table_from_json(covid19tests, 'covid19_tests', cur)


# Commit the changes and close the connection
conn.commit()
conn.close()
