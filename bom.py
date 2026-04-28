import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")

tables = soup.find_all("table")

print("Number of tables found:", len(tables))

# safety check
if len(tables) <= 19:
    raise Exception("Table index 19 not found - BOM page structure changed")

table = tables[19]

rows = []
for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        rows.append(cols)

df = pd.DataFrame(rows)
df.to_csv("bom_rainfall.csv", index=False)
