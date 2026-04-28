import requests
from bs4 import BeautifulSoup

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

print("Fetching BOM page...")

r = requests.get(url, timeout=30)

print("Status code:", r.status_code)
print("Final URL:", r.url)
print("HTML length:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Tables found:", len(tables))

# print first few table sizes (important)
for i, t in enumerate(tables[:10]):
    print(f"Table {i} rows:", len(t.find_all('tr')))

print("DONE")
