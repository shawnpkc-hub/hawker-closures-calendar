import os
os.makedirs("docs", exist_ok=True)
import pandas as pd
import requests
from ics import Calendar, Event
from datetime import datetime
import os

# ensure docs folder exists
os.makedirs("docs", exist_ok=True)

# Official data.gov.sg API endpoint
DATA_URL = "https://data.gov.sg/api/action/datastore_search?resource_id=8e6b0f1c-0a0a-4c4d-9c1c-3c4a4b0fdf6c&limit=500"

print("Downloading dataset...")

import os

API_KEY = os.getenv("DATA_GOV_SG_API_KEY")

headers = {
    "api-key": API_KEY
}

response = requests.get(DATA_URL, headers=headers)
response.raise_for_status()

data = response.json()
records = data["result"]["records"]

df = pd.DataFrame(records)

print("Columns detected:", df.columns.tolist())

cal = Calendar()

def parse_date(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "")).date()
    except:
        return None

events_added = 0

for _, row in df.iterrows():

    name = row.get("hawker_centre") or row.get("name")
    start = parse_date(row.get("start_date"))
    end = parse_date(row.get("end_date"))
    desc = row.get("description", "Hawker Centre Closure")

    if not name or not start:
        continue

    e = Event()
    e.name = f"{name} – CLOSED"
    e.begin = start
    e.end = end or start
    e.make_all_day()
    e.description = desc

    cal.events.add(e)
    events_added += 1

print("Events added:", events_added)

with open("docs/hawker_closures.ics", "w") as f:
    f.writelines(cal)

print("Calendar written successfully.")
