import requests
from bs4 import BeautifulSoup

url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDN60169.html"

print("Fetching BOM page...")

r = requests.get(url, timeout=30)

print("Status:", r.status_code)
print("Length:", len(r.text))

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print("Tables found:", len(tables))

# STOP HERE (no indexing yet)
print("Script finished safely")
