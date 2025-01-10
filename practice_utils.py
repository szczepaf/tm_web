import requests
import datetime
import pytz
import logging
import os
import mysql.connector
import json


DB_USERNAME = os.getenv("DB_USERNAME")
DB_PW = os.getenv("DB_PASSWORD")

EVENT_TYPE_ID = 1
EVENTS_TO_LOAD = 3
prague_timezone = pytz.timezone('Europe/Prague')

class Practice:
    def __init__(self, name: str, start_time: datetime.datetime, end_time: datetime.datetime, location: str):
        self.name = name
        self.start_time = start_time.replace(tzinfo=pytz.utc).astimezone(prague_timezone)
        self.end_time = end_time.replace(tzinfo=pytz.utc).astimezone(prague_timezone)
        self.location = location

    def get_date(self):
        return self.start_time.strftime("%d. %m.")

    def get_start(self):
        return self.start_time.strftime("%H:%M")

    def get_end(self):
        return self.end_time.strftime("%H:%M")

    def __str__(self):
        return f'name: {self.name}, start_time: {self.start_time.strftime("%d. %m. %H:%M")}'

def get_today_str():
    today = datetime.date.today()
    formatted = today.strftime("%Y%m%d")
    print(formatted)
    return formatted

def connect_to_db(db_username, db_password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=db_username,
            password=db_password,
            database="attendance"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def load_events_from_db(db_username, db_password):
    try:
        connection = connect_to_db(db_username, db_password)
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT * FROM events WHERE end_time > %s and type = "Trénink"
            ORDER BY start_time ASC
        """

        now = datetime.datetime.now()
        cursor.execute(query, (now,))
        events = cursor.fetchall()
        return events
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_trainings():
    events = load_events_from_db(DB_USERNAME, DB_PW)
    practices = []
    for practice_raw in events:
        name = practice_raw["name"]
        start_time = practice_raw["start_time"]
        end_time = practice_raw["end_time"]
        address = practice_raw["address"]
        type = practice_raw["type"]
        if type != "Trénink":
            continue
        practice = Practice(name, start_time, end_time, address)
        practices.append(practice)

    return practices[:EVENTS_TO_LOAD]
