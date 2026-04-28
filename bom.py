import requests
from bs4 import BeautifulSoup

print("START BOM TEST")

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

r = requests.get(url, timeout=30)

print("HTTP status:", r.status_code)
print("HTML size:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Total tables found:", len(tables))

# safety check for your chosen index
if len(tables) <= 19:
    print("TABLE 19 NOT AVAILABLE")
    print("Stopping safely")
    exit()

print("TABLE 19 EXISTS - extracting...")

table = tables[19]

rows = []

for tr in table.find_all("tr"):
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        rows.append(cols)

print("Rows extracted:", len(rows))

# show a small preview (no file output yet)
print("\n--- SAMPLE ROWS ---")
for r in rows[:5]:
    print(r)

print("END SUCCESS")
