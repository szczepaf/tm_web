import requests
import datetime
import pytz

import os

# Assuming you have a UTC datetime object


IMPORTER_LOGIN = os.getenv("TYMY_USERNAME")
IMPORTER_PWD = os.getenv("TYMY_PASSWORD")
print(IMPORTER_LOGIN)
print(IMPORTER_PWD)

EVENT_TYPE_ID = 1
EVENTS_TO_LOAD = 3
prague_timezone = pytz.timezone('Europe/Prague')

class Practice:
    def __init__(self, name: str, start_time: datetime.datetime, end_time: datetime.datetime, location: str, map_link: str):
        self.name = name
        self.start_time = start_time.replace(tzinfo=pytz.utc).astimezone(prague_timezone)
        self.end_time = end_time.replace(tzinfo=pytz.utc).astimezone(prague_timezone)
        self.location = location
        self.map_link = map_link
    
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

def get_trainings():
    url = "https://monkeys.tymy.cz/api/events"
    params = {
        "login": IMPORTER_LOGIN,
        "password": IMPORTER_PWD,
        "limit": EVENTS_TO_LOAD,
        "filter": f"startTime>{get_today_str()}~eventTypeId={EVENT_TYPE_ID}",
        "order": "startTime__ASC",
    }
    response = requests.get(url, params=params)
    practices = []
    if response.status_code != 200:
        return practices
    for practice_json in response.json()["data"]:
        name = practice_json["caption"]
        print(practice_json["startTime"])
        start_time = datetime.datetime.strptime(practice_json["startTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
        end_time = datetime.datetime.strptime(practice_json["endTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
        location = practice_json["place"]
        map_link = practice_json["link"]
        practice = Practice(name, start_time, end_time, location, map_link)
        practices.append(practice)
    return practices
