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
# print(world_population)


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
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Ensure the structure of the JSON data and the keys match the expected format
    # if isinstance(data, dict):
    cur.execute(f'''
            CREATE TABLE {table_name} (
            country VARCHAR(255),
            population INTEGER,
            yearly_change VARCHAR(255),
            net_change INTEGER,
            density INTEGER,
            land_area INTEGER,
            migrants_net INTEGER,
            fert_rate VARCHAR(255),
            med_age VARCHAR(255),
            urban_pop_percent VARCHAR(255),
            world_share VARCHAR(255)
        )'''
    )
    for data in json_data:
        cur.execute(f"""
            INSERT INTO {table_name} (
                country, population, yearly_change, net_change, density,
                land_area, migrants_net, fert_rate, med_age, urban_pop_percent, world_share
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )""", (
                data['Country (or dependency)'],
                data['Population (2020)'] if data['Population (2020)'] else None,
                data['Yearly Change'],
                data['Net Change'] if data['Net Change'] else None ,
                data['Density'] if 'Density' in data else None,
                data['Land Area'] if data['Land Area'] else None ,
                data['Migrants (net)'] if  data['Migrants (net)'] else None ,
                data['Fert. Rate'] if data['Fert. Rate'] else None ,
                data['Med. Age'] if data['Med. Age'] else None ,
                data['Urban Pop %'] if data['Urban Pop %'] else None ,
                data['World Share'] if data['World Share'] else None 
            )
        
        )
        
# test dataset

def create_test_table_from_json(json_data, table_name, cur):
    print('hey')
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
    # count=0
    # Insert data into the table
    for item in json_data:
        if 'TotalTests' in item and item['TotalTests'] == 'NA':
            item['TotalTests'] = None
        if 'Tests' in item and '1M pop' in item['Tests'] and item['Tests']['1M pop'] == 'NA':
            item['Tests']['1M pop'] = None
        if '1 Testevery X ppl' in item and item['1 Testevery X ppl'] == 'NA':
            item['1 Testevery X ppl'] = None

    with open(covid19tests, 'w') as file:
        json.dump(json_data, file, indent=4)

    for data in json_data:
        # Insert the data into the table
        cur.execute(f"""
            INSERT INTO {table_name} (
                date, country_or_other, total_tests, population, tests_per_1m_pop, test_every_x_ppl
            ) VALUES (
                %s, %s, %s, %s, %s, %s
            )""", (
                data['Date'],
                data['Country,Other'],
                data['TotalTests'],
                data['Population'],
                data['Tests']['1M pop'],
                data['1 Testevery X ppl']
            )
        )

# Call the function with the JSON data, table name, and cursor
insert_json_data_to_postgres(covid19_africa, "covid19africa", cur)
insert_json_data_to_postgres(covid19_asia, 'covid19_asia', cur)
insert_json_data_to_postgres(covid19_europe, 'covid19_europe', cur)
insert_json_data_to_postgres(covid19_northamerica, 'covid19_northamerica', cur)
insert_json_data_to_postgres(covid19_southamerica, 'covid19_southamerica', cur)
insert_json_data_to_postgres(covid19_world, 'covid19_world', cur)
create_table_from_json(world_population, 'world_population', cur)

# Work on this!
# create_test_table_from_json(covid19tests, 'covid19_tests', cur)

# Commit the changes and close the connection

# Queries



conn.commit()
conn.close()
