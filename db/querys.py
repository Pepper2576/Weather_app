import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

connection = psycopg2.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD")
)

curr = connection.cursor()

def add_weather_data(date, temperature):
    curr.execute("INSERT INTO weather_data (date, temperature) VALUES (%s, %s)", (date, temperature))
    connection.commit()
    print("Data added successfully")
    

