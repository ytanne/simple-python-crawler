import dryscrape
from bs4 import BeautifulSoup

session = dryscrape.Session()
session.visit("https://www.zakon.kz/5003300-v-kostanayskoy-oblasti-pogib.html")
response = session.body()
soup = BeautifulSoup(response, features="lxml")
print(soup.find(id="zkn_comments"))