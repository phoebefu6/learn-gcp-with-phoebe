"""Fetch the seeded Chicago taxi sample from the City of Chicago data portal (Socrata API).

Source : City of Chicago, "Taxi Trips (2013-2023)", dataset wrvz-psew,
         https://data.cityofchicago.org/Transportation/Taxi-Trips-2013-2023-/wrvz-psew
         Licence: City of Chicago data portal Terms of Use (licenseId SEE_TERMS_OF_USE).
         BigQuery hosts the same trips as bigquery-public-data.chicago_taxi_trips.taxi_trips.
Method : one seeded 15-minute slot per calendar month, 2013-01 to 2023-12 (132 slots).
         Trip start times are rounded to 15 minutes at source, so a slot is an exact-match filter.
         Up to 150 trips per slot, ordered by trip_id (deterministic).
         Also fetches the exact January 2019 trip count per pickup community area (the
         partition + cluster rungs of the cost ladder), and the same count for each day of
         January 2019 (the day partitions the cluster model sorts).
Output : <out>/slots/*.json, <out>/jan2019_ca.json, <out>/view.json
Run    : python fetch-taxi-sample.py <out dir>      (stdlib only; fetched 2026-11-03)
"""
import json, os, random, sys, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "https://data.cityofchicago.org/resource/wrvz-psew.json"
SEED, PER_SLOT = 20261103, 150
OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, "slots"), exist_ok=True)


def get(params, path):
    if os.path.exists(path):
        return
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=180) as r:
        data = r.read()
    open(path, "wb").write(data)


rng = random.Random(SEED)
slots = []
for y in range(2013, 2024):
    for m in range(1, 13):
        day = rng.randint(1, 28)
        hour = rng.randint(7, 22)  # daytime and evening, when trips exist in every year
        minute = rng.choice([0, 15, 30, 45])
        slots.append(f"{y}-{m:02d}-{day:02d}T{hour:02d}:{minute:02d}:00")

jobs = [({"$where": f"trip_start_timestamp='{s}'", "$order": "trip_id", "$limit": PER_SLOT},
         os.path.join(OUT, "slots", s.replace(":", "") + ".json")) for s in slots]
jobs.append(({"$select": "pickup_community_area,count(trip_id) as n",
              "$where": "trip_start_timestamp>='2019-01-01T00:00:00' AND trip_start_timestamp<'2019-02-01T00:00:00'",
              "$group": "pickup_community_area", "$limit": 200}, os.path.join(OUT, "jan2019_ca.json")))
os.makedirs(os.path.join(OUT, "jan2019_days"), exist_ok=True)
for d in range(1, 32):
    a, b = f"2019-01-{d:02d}T00:00:00", (f"2019-01-{d + 1:02d}T00:00:00" if d < 31 else "2019-02-01T00:00:00")
    jobs.append(({"$select": "pickup_community_area,count(trip_id) as n",
                  "$where": f"trip_start_timestamp>='{a}' AND trip_start_timestamp<'{b}'",
                  "$group": "pickup_community_area", "$limit": 200},
                 os.path.join(OUT, "jan2019_days", f"2019-01-{d:02d}.json")))
with ThreadPoolExecutor(3) as ex:
    list(ex.map(lambda j: get(*j), jobs))
urllib.request.urlretrieve("https://data.cityofchicago.org/api/views/wrvz-psew.json", os.path.join(OUT, "view.json"))
print("slots", len(slots), "files", len(os.listdir(os.path.join(OUT, "slots"))))
