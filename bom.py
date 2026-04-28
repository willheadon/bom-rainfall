import requests
from bs4 import BeautifulSoup

print("START BOM TEST")

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

# make request look like a real browser
headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)

print("HTTP status:", r.status_code)
print("HTML size:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Total tables found:", len(tables))

# keep your table 19 approach
if len(tables) <= 19:
    print("TABLE 19 NOT AVAILABLE")
    exit()

print("TABLE 19 EXISTS")

table = tables[19]

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        rows.append(cols)

print("Rows extracted:", len(rows))

print("END SUCCESS")
