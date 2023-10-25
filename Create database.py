import csv
import psycopg2

conn = psycopg2.connect(database="flask_db",  
                        user="sequel", 
                        password="7b80eefa",  
                        host="localhost", port="5432")

cur = conn.cursor() 
conn.commit() 
cur.close() 
conn.close() 
