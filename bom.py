import requests
from bs4 import BeautifulSoup
import pandas as pd

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
    raise Exception("Table 19 not found")

table = tables[19]

rows = []
for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        rows.append(cols)

print("Rows extracted:", len(rows))

df = pd.DataFrame(rows)
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

df["LastUpdated"] = now
# tidy for Power BI
df = df.dropna(axis=1, how='all')

output_file = "bom_rainfall.csv"
df.to_csv(output_file, index=False)

print("CSV WRITTEN:", output_file)
print(df.head())
