import requests
from bs4 import BeautifulSoup as bs
import subprocess
import pymongo
from pymongo import MongoClient
import numpy as np
import re

links = []
my_location = "Kastelorizo"
i = 0
headers = []

in_month = 7
in_day = 25
in_year = 2021
out_month = 7
out_day = 30
out_year = 2021
people = 2
city = "Kastelorizo"
country = "Greece"


link = "https://www.booking.com/searchresults.html?checkin_month={in_month}&checkin_monthday={in_day}" \
    "&checkin_year={in_year}&checkout_month={out_month}&checkout_monthday={out_day}&checkout_year={out_year}" \
    "&group_adults={people}&group_children=0&order=price&ss={city}%2C%20{country}" \
        .format(in_month=in_month,
                in_day=in_day,
                in_year=in_year,
                out_month=out_month,
                out_day=out_day,
                out_year=out_year,
                people=people,
                city=city,
                country=country)

print(link)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"} # Windows 10 with Google Chrome

main_page = requests.get(link, headers = headers)

#Convert to bs object
soup = bs(main_page.content, 'lxml') #html.parser

properties = soup.find('div', class_='sr_header--title').text.strip()

number = re.sub("[^0-9]", "", properties)
print(number+" Hotels")
loopnumber = round(np.ceil(int(number)/25)) #vriskw ton arithmo twn selidwn gia na kanw loop oles tis selides
print(str(loopnumber)+" Pages")

pages = np.arange(0, loopnumber, 1)
print(pages)

for page in pages:
    temp_link = link+"&rows=25&offset="+str(page*25) #"https://www.booking.com/searchresults.gr.html?checkin_month=6&checkin_monthday=25&checkin_year=2021&checkout_month=6&checkout_monthday=30&checkout_year=2021&group_adults=2&group_children=0&order=price&ss=Kastelorizo%2C%20Greece&offset=0"
    print(temp_link)
    offset_page = requests.get(temp_link, headers = headers)
    soup = bs(offset_page.content, 'lxml')
    #ftiaxnw lista me ola ta urls twn ksenodoxeiwn
    for a in soup.find_all('a', {'class':'hotel_name_link'}):
        links.insert(0, a['href'].strip())
links.reverse()
print(str(len(links))+" urls found")

while i < 2: #len(links):
    page = requests.get('https://booking.com'+links[i])
    soup = bs(page.content, 'lxml')
    title = soup.find('h2', class_='hp__hotel-name').text.strip()
    print(title)
    address = soup.find('span', class_='hp_address_subtitle').text.strip()
    print(address)
    reviews = soup.find('div', class_='_6a1b6ff88e').text.strip()
    print(reviews)
    rating = soup.find('div', class_='e5a32fd86b').text.strip()
    print(rating)
    i = i+1
