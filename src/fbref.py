import requests 
import re
from bs4 import BeautifulSoup

headers = { "User-Agent : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4124.104 Safari/537.36 Edge/18.18362'" } 
r= requests.get('https://fbref.com/en/comps/56/history/Austrian-Bundesliga-Seasons')

f = open("demofile3.html", "w")
f.write(r.text)
f.close()

soup = BeautifulSoup(r.text, "html.parser") 
print("----")
rows=soup.select("#switcher_stats_squads_misc table tr")
print("----",rows)
for row in rows:
    tds=row.select("td")
    aTag=row.select("th a")
    if len(aTag)==0:
        continue
    print("---------")
    print("name: ",aTag[0].get_text() )
    for count, item in enumerate(tds, start=0):   # default is zero
        print("ii: ",count," item: ",item.get_text()  )
    print("---------")