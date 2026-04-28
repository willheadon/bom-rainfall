import requests
from bs4 import BeautifulSoup
import pandas as pd

print("STARTING BOM SCRIPT")

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

try:
    r = requests.get(url, timeout=30)
    print("HTTP status:", r.status_code)

    r.raise_for_status()

except Exception as e:
    print("ERROR: failed to fetch BOM page")
    print(e)
    raise

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Tables found:", len(tables))

# ---- KEEP YOUR TABLE 19 LOGIC ----
if len(tables) <= 19:
    print("ERROR: table index 19 not available")
    print("Only found:", len(tables), "tables")
    raise Exception("Missing table[19] in BOM response")

table = tables[19]

print("Using table 19 successfully")

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    
    if cols:
        rows.append(cols)

if not rows:
    print("ERROR: table 19 found but no data rows extracted")
    raise Exception("Empty dataset")

df = pd.DataFrame(rows)

# clean for Power BI stability
df = df.dropna(axis=1, how='all')

output_file = "bom_rainfall.csv"
df.to_csv(output_file, index=False)

print("SUCCESS: wrote", output_file)
print(df.head())
