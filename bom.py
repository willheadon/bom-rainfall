import requests
from bs4 import BeautifulSoup
import pandas as pd
import traceback

print("START SCRIPT")

try:
    url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

    print("Fetching BOM...")
    r = requests.get(url, timeout=30)
    print("Status:", r.status_code)

    soup = BeautifulSoup(r.text, "html.parser")

    tables = soup.find_all("table")
    print("Tables found:", len(tables))

    print("Attempting to access table 19...")

    table = tables[19]   # <-- we keep your logic

    rows = []
    for tr in table.find_all("tr"):
        cols = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cols:
            rows.append(cols)

    df = pd.DataFrame(rows)
    df.to_csv("bom_rainfall.csv", index=False)

    print("SUCCESS")

except Exception as e:
    print("ERROR OCCURRED:")
    print(e)
    traceback.print_exc()
    raise
