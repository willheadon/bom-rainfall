import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

print("Starting BOM extraction...")

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    print("Page downloaded OK")
except Exception as e:
    print("ERROR fetching BOM page:", e)
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")
print(f"Total tables found: {len(tables)}")

# safety check before using index 19
if len(tables) <= 19:
    print("ERROR: Expected at least 20 tables, but found fewer.")
    sys.exit(1)

table = tables[19]

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        rows.append(cols)

if not rows:
    print("ERROR: No data rows extracted from table.")
    sys.exit(1)

df = pd.DataFrame(rows)

output_file = "bom_rainfall.csv"
df.to_csv(output_file, index=False)

print(f"Success! Wrote {output_file}")
print(df.head())
