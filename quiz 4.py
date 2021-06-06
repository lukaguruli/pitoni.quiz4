import requests
from bs4 import BeautifulSoup
import sqlite3
from tqdm import tqdm

conn = sqlite3.connect('covid19.sqlite3')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS covid19 (
country VARCHAR(10), total VARCHAR(20))''')

r = requests.get('https://www.worldometers.info/coronavirus/')
soup = BeautifulSoup(r.text, 'html.parser')
co = soup.find_all("a", {"class": "mt_a"})
countries = []
for c in tqdm(co):
    countries.append(c.text)
    if c == soup.find_all("a", {"class": "mt_a"})[15]:
        break
amount = []
td = soup.findAll('tbody')
table = str(td[0]).split('<tr style="">')
table = table[1:17]
for td in tqdm(table):
    text = td.split('</td>\n')
    total = text[2].split('>')
    total = total[1]
    amount.append(total)

for i in tqdm(range(16)):
    cur.execute('''INSERT INTO covid19(
    country, total) VALUES(?,?)''', (countries[i], amount[i]))
    conn.commit()
conn.close()