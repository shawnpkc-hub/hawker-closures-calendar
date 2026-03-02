import os
os.makedirs("docs", exist_ok=True)
import pandas as pd
import requests
from ics import Calendar, Event
from datetime import datetime

DATA_URL = "https://data.gov.sg/api/action/datastore_search?resource_id=8e6b0f1c-0a0a-4c4d-9c1c-3c4a4b0fdf6c&limit=500"

data = requests.get(DATA_URL).json()
df = pd.DataFrame(data["result"]["records"])

cal = Calendar()

def add_event(name, start, end, remark):
    if pd.isna(start):
        return

    start_date = datetime.strptime(start, "%d/%m/%Y")
    end_date = datetime.strptime(end, "%d/%m/%Y")

    e = Event()
    e.name = f"{name} – CLOSED"
    e.begin = start_date.date()
    e.end = end_date.date()
    e.make_all_day()
    e.description = f"NEA Hawker Closure ({remark})"

    cal.events.add(e)

for _, row in df.iterrows():
    name = row["Name"]

    add_event(name, row["Q1 Cleaningstartdate"], row["Q1 Cleaningenddate"], "Cleaning")
    add_event(name, row["Q2 Cleaningstartdate"], row["Q2 Cleaningenddate"], "Cleaning")
    add_event(name, row["Q3 Cleaningstartdate"], row["Q3 Cleaningenddate"], "Cleaning")
    add_event(name, row["Q4 Cleaningstartdate"], row["Q4 Cleaningenddate"], "Cleaning")
    add_event(name, row["Other Works Startdate"], row["Other Works Enddate"], "Renovation")

with open("docs/hawker_closures.ics", "w") as f:
    f.writelines(cal)
print("Calendar generated:", len(cal.events), "events")
