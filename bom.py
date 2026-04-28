import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

print("Fetching BOM page...")

r = requests.get(url, timeout=30)

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Tables found:", len(tables))

# safety check (DO NOT REMOVE)
if len(tables) <= 19:
    raise Exception(f"Expected table 19 but only found {len(tables)} tables")

table = tables[19]

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        rows.append(cols)

df = pd.DataFrame(rows)

# clean output for Power BI
df = df.dropna(axis=1, how='all')

df.to_csv("bom_rainfall.csv", index=False)

print("SUCCESS: CSV written")
