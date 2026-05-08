import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone, timedelta

print("START BOM RUN")

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Tables found:", len(tables))

if len(tables) <= 19:
    raise Exception("Required tables not found")

# --- helper function ---
def extract_rows(table):
    rows = []
    for tr in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            rows.append(cols)
    return rows

# --- extract tables ---
table_williams = tables[19]
table_patterson = tables[18]

rows_williams = extract_rows(table_williams)
rows_patterson = extract_rows(table_patterson)

print("Williams rows:", len(rows_williams))
print("Patterson rows:", len(rows_patterson))

# --- create dataframes ---
df_williams = pd.DataFrame(rows_williams)
df_patterson = pd.DataFrame(rows_patterson)

# --- NSW fixed time (ignore daylight savings) ---
nsw_offset = timezone(timedelta(hours=10))
now_nsw = datetime.now(timezone.utc).astimezone(nsw_offset)

timestamp = now_nsw.strftime("%Y-%m-%d %H:%M:%S")

df_williams["LastUpdated_NSW"] = timestamp
df_patterson["LastUpdated_NSW"] = timestamp

# --- tidy for Power BI ---
df_williams = df_williams.dropna(axis=1, how='all')
df_patterson = df_patterson.dropna(axis=1, how='all')

# --- output files ---
output_williams = "bom_rainfall_williams.csv"
output_patterson = "bom_rainfall_patterson.csv"

df_williams.to_csv(output_williams, index=False)
df_patterson.to_csv(output_patterson, index=False)

print("CSV WRITTEN:", output_williams)
print(df_williams.head())

print("CSV WRITTEN:", output_patterson)
print(df_patterson.head())

print("END SUCCESS")
