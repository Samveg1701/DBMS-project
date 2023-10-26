# # # 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project'
import os
# import csv
# # import time
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

# world population
def create_table_from_json(json_data, table_name, cur):
    # formatting of the dictionary
    for item in json_data:
        if 'Density (P' in item:
            density_value = item.pop('Density (P')
            if "Km²)" in density_value:
                item['Density (P/Km²)'] = { "Km²": density_value["Km²)"] }

    # Save the modified data back to the JSON file
    with open(worldpopulation, 'w') as file:
        json.dump(json_data, file, indent=4)

    # Ensure the structure of the JSON data and the keys match the expected format
    for data in json_data:
        if isinstance(data, dict):
            cur.execute(f"""
                INSERT INTO {table_name} (
                    country_or_dependency, population_2020, yearly_change, net_change, density_per_km2, land_area_km2, migrants_net, fertility_rate, median_age, urban_pop_percentage, world_share
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )""", (
                    data.get('Country (or dependency)'),
                    data.get('Population (2020)'),
                    data.get('Yearly Change'),
                    data.get('Net Change'),
                    data.get('Density (P', {}).get('Km²'),
                    data.get('Land Area (Km²)'),
                    data.get('Migrants (net)'),
                    data.get('Fert. Rate'),
                    data.get('Med. Age'),
                    data.get('Urban Pop %'),
                    data.get('World Share')
                )
            )
        
# test dataset
def create_test_table_from_json(json_data, table_name, cur):
    # Drop the table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create a new table
    cur.execute(f'''
        CREATE TABLE {table_name} (
            date VARCHAR(30),
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
create_test_table_from_json(covid19tests, 'covid19_tests', cur)


# Commit the changes and close the connection
conn.commit()
conn.close()
