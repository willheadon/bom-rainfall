import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback

print("SCRIPT STARTED")

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

r = requests.get(url, timeout=30)

print("HTTP:", r.status_code)
print("HTML size:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Tables found:", len(tables))

try:
    print("Attempting table[19]")

    table = tables[19]

    rows = []
    for tr in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            rows.append(cols)

    df = pd.DataFrame(rows)
    df.to_csv("bom_rainfall.csv", index=False)

    print("SUCCESS")

except Exception as e:
    print("FAILED WITH ERROR:")
    print(e)
    traceback.print_exc()
    raise
