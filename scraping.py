import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
from datetime import datetime

def fetch_temperatures(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    calendar_items = soup.select('div.past-calender-box div.past-calender-item:not(.past)')
    
    high_temps = [item.find('p', class_='temp high-temp red').get_text() for item in calendar_items if item.find('p', class_='temp high-temp red')]
    low_temps = [item.find('p', class_='temp low-temp blue').get_text() for item in calendar_items if item.find('p', class_='temp low-temp blue')]
    return high_temps, low_temps

def parse_temperature(temps):
    return [float(temp.replace('℃', '')) for temp in temps]

def insert_data_to_db(cur, data):
    insert_sql = "INSERT INTO database (date, high_temp, low_temp, sleep_time) VALUES (?, ?, ?, ?)"
    cur.executemany(insert_sql, data)

def create_database(cur):
    sql_create_table = '''
    CREATE TABLE IF NOT EXISTS database (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME,
        high_temp REAL,
        low_temp REAL,
        sleep_time REAL
    );
    '''
    cur.execute(sql_create_table)

def main():
    # URLs for temperature data
    url_dec = 'https://tenki.jp/amp/past/2023/12/weather/3/15/47682/'
    url_jan = 'https://tenki.jp/amp/past/2024/01/weather/3/15/47682/'

    # Fetch and parse temperature data
    high_temp_dec, low_temp_dec = fetch_temperatures(url_dec)
    high_temp_jan, low_temp_jan = fetch_temperatures(url_jan)

    high_temps = parse_temperature(high_temp_dec + high_temp_jan)
    low_temps = parse_temperature(low_temp_dec + low_temp_jan)

    # Read sleep data
    df = pd.read_csv('./dspro_last_assignment_local_data.csv')
    sleep_times = df['睡眠時間'].tolist()
    dates = pd.to_datetime(df['日付']).dt.date.tolist()

    # Prepare data for insertion
    data = [(str(dates[i]), high_temps[i], low_temps[i], sleep_times[i]) for i in range(len(sleep_times))]

    # Database operations
    db_path = './database.sqlite'
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        create_database(cur)
        insert_data_to_db(cur, data)
        conn.commit()

if __name__ == "__main__":
    main()
