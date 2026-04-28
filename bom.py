import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

tables = soup.find_all("table")
table = tables[19]

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    
    # skip empty rows
    if not cols:
        continue

    rows.append(cols)

df = pd.DataFrame(rows)

# remove completely empty columns (important for Power BI)
df = df.dropna(axis=1, how='all')

df.to_csv("bom_rainfall.csv", index=False)

print("CSV written successfully")
