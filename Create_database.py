# # # 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project'
import os
# import csv
# # import time
import psycopg2
import json
from datetime import datetime
import pandas as pd


# C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/DBMS project/complete.json
covid19africa = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_africa.json'
covid19asia = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_asia.json'
covid19europe = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_europe.json'
covid19northamerica = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_northamerica.json'
covid19oceania = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_oceania.json'
covid19southamerica = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/New dataset/covid19_southamerica.json'
covid19tests = 'C:/Users/asus/OneDrive/Desktop/University/Semester 7/DBMS/Old dataset/covid19_tests.json'
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
# print(covid19_africa)
# test day wise
with open(covid19asia, 'r') as file:
    covid19_asia = json.load(file)

with open(covid19europe, 'r') as file:
    covid19_europe = json.load(file)

with open(covid19northamerica, 'r') as file:
    covid19_northamerica = json.load(file)

with open(covid19oceania, 'r') as file:
    covid19_oceania = json.load(file)

with open(covid19southamerica, 'r') as file:
    covid19_southamerica = json.load(file)

with open(covid19tests, 'r') as file:
    covid19_tests = json.load(file)

with open(covid19world, 'r') as file:
    covid19_world = json.load(file)

with open(worldpopulation, 'r') as file:
    world_population = json.load(file)
# print(world_population)

# print(covid19_tests)
def insert_json_data_to_postgres(json_data, table_name, cur):
    # Drop the table if it already exists
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Create a new table
    cur.execute(f'''
        CREATE TABLE {table_name} (
            observation_date DATE,
            country VARCHAR(255),
            region VARCHAR(255),
            confirmed float,
            deaths float,
            recovered float,
            active float
        )
    ''')

    # Insert data into the table
    for data in json_data:

        if 'Confirmed' in data and (data['Confirmed'] == 'NA' or data['Confirmed'] == ''):
            data['Confirmed'] = 0
        if 'Deaths' in data and (data['Deaths'] == 'NA' or data['Deaths'] == ''):
            data['Deaths'] = 0
        if 'Recovered' in data and (data['Recovered'] == 'NA' or data['Recovered'] == ''):
            data['Recovered'] = 0
        if 'Active' in data and (data['Active'] == 'NA' or data['Active'] == ''):
            data['Active'] = 0

        if isinstance(data, dict) and all(key in data for key in ['ObservationDate', 'Country_Region', 'Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active']):
            observation_date = datetime.strptime(data["ObservationDate"], '%Y-%m-%d').date()
            cur.execute(f"""
                INSERT INTO {table_name} (
                    observation_date, country, region, confirmed, deaths, recovered, active
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s
                )""", (
                    observation_date,
                    data["Country_Region"],
                    data["Province_State"],
                    data["Confirmed"],
                    data["Deaths"],
                    data["Recovered"],
                    float(data["Active"])
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
    # cur.execute(f"SELECT * FROM world_population")
    # records = cur.fetchall()
    # for record in records:
    #     print(records)
        
# test dataset

from datetime import datetime

def create_test_table_from_json(json_data, table_name, cur):
    # print('hey')
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")

    cur.execute(f'''
        CREATE TABLE {table_name} (
            date DATE,
            country_or_other VARCHAR(255),
            total_tests FLOAT,
            population VARCHAR(255),
            tests_per_1m_pop VARCHAR(255),
            test_every_x_ppl VARCHAR(255)
        )
    ''')

    for data in json_data:
        if 'TotalTests' in data and data['TotalTests'] == 'NA':
            data['TotalTests'] = 0
        if 'Tests/1M pop' in data and data['Tests/1M pop'] == 'NA':
            data['Tests/1M pop'] = None
        if '1 Testevery X ppl' in data and data['1 Testevery X ppl'] == 'NA':
            data['1 Testevery X ppl'] = None

        if all(key in data for key in ['Date', 'Country,Other', 'TotalTests', 'Population', 'Tests/1M pop', '1 Testevery X ppl']):
            observation_date = datetime.strptime(data["Date"], '%Y-%m-%d').date()
            cur.execute(f"""
                INSERT INTO {table_name} (
                    date, country_or_other, total_tests, population, tests_per_1m_pop, test_every_x_ppl
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )""", (
                    observation_date,
                    data['Country,Other'],
                    float(data['TotalTests']),
                    data['Population'],
                    data['Tests/1M pop'],
                    data['1 Testevery X ppl']
                )
            )

    # cur.execute(f"SELECT * FROM {table_name}")
    # records = cur.fetchall()
    # for record in records:
    #     print(record)

# Example usage
json_data = covid19_tests

# Assuming 'cur' is your database cursor
# create_test_table_from_json(json_data, 'covid19_tests', cur)

# Call the function with the JSON data, table name, and cursor
# insert_json_data_to_postgres(covid19_africa, "covid19_africa", cur)
# insert_json_data_to_postgres(covid19_asia, 'covid19_asia', cur)
# insert_json_data_to_postgres(covid19_europe, 'covid19_europe', cur)
# insert_json_data_to_postgres(covid19_northamerica, 'covid19_northamerica', cur)
# insert_json_data_to_postgres(covid19_southamerica, 'covid19_southamerica', cur)
# insert_json_data_to_postgres(covid19_oceania, 'covid19_oceania', cur)
# insert_json_data_to_postgres(covid19_world, 'covid19_world', cur)
# create_table_from_json(world_population, 'world_population', cur)

# Work on this!
# create_test_table_from_json(covid19_tests, 'covid19_tests', cur)

# Commit the changes and close the connection

# Queries
def select_total_continents(tablename):
    cur.execute(f"SELECT observation_date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) FROM {tablename} GROUP BY observation_date")
    rows = cur.fetchall()
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows


def country(tablename, country_name, specified_date):
    # cur.execute(f"SELECT observation_date, country, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) FROM {tablename} WHERE country = %s GROUP BY observation_date, country", (country_name,))
    cur.execute(f"SELECT observation_date, country, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) FROM {tablename} WHERE country = %s AND observation_date = %s GROUP BY observation_date, country", (country_name, specified_date))

    rows = cur.fetchall()
    df = pd.DataFrame(rows, columns=['Observation Date', 'Country', 'Total Confirmed', 'Total Deaths', 'Total Recovered', 'Total Active'])
    print(df)
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows

def select_data_between_dates(tablename, date1, date2):
    # cur.execute(f"SELECT observation_date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) FROM {tablename} WHERE observation_date BETWEEN " + date1 + " AND " + date2 + " GROUP BY observation_date")
    cur.execute(f"SELECT observation_date, SUM(confirmed), SUM(deaths), SUM(recovered), SUM(active) FROM {tablename} WHERE observation_date BETWEEN %s AND %s GROUP BY observation_date", (date1, date2))

    rows = cur.fetchall()
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows     

# dates = select_data_between_dates("covid19africa", "2020-01-27", "2020-02-15")
# print(dates)

def select_total_countries():
    cur.execute(f"SELECT DISTINCT country FROM covid19_world")
    rows = cur.fetchall()
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows

tablename = "covid19_world"  # Assuming tablename is a string
select_total_continents(tablename)


def select_world_population():
    cur.execute(f"SELECT * FROM world_population")
    rows = cur.fetchall()
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows
    
def select_tests(tablename):
    # cur.execute(f"SELECT * FROM covid19_tests")
    cur.execute(f"SELECT date, SUM(total_tests) FROM covid19_tests GROUP BY date")

    rows = cur.fetchall()
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows
    
def join_continents():
    cur.execute(f"""SELECT 
    observation_date, 
    SUM(confirmed) as total_confirmed,
    SUM(deaths) as total_deaths,
    SUM(recovered) as total_recovered,
    SUM(active) as total_active
    FROM (
    SELECT observation_date, confirmed, deaths, recovered, active FROM covid19_africa
    UNION ALL
    SELECT observation_date, confirmed, deaths, recovered, active FROM covid19_asia
    UNION ALL
    SELECT observation_date, confirmed, deaths, recovered, active FROM covid19_europe
    UNION ALL
    SELECT observation_date, confirmed, deaths, recovered, active FROM covid19_north_america
    UNION ALL
    SELECT observation_date, confirmed, deaths, recovered, active FROM covid19_south_america
) as all_continents
GROUP BY observation_date;
""")
    rows = cur.fetchall()
    if not rows:
            print("No rows found.")
    else:
        # for row in rows:
        #     print(row)
        return rows

total_continents = country("covid19africa", "Egypt", "2020-02-14")
# print(select_tests(covid19_tests))
# test= select_tests(covid19_tests)
print(total_continents)
# print(total_continents)
conn.commit()
conn.close()
