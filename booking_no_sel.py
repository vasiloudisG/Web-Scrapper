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
facilities = []
scores = []

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
    print(links)

print(str(len(links))+" urls found")

while i < 2: #len(links):
    page = requests.get('https://booking.com'+links[i], headers = headers)
    soup = bs(page.content, 'lxml')

    title = soup.find('h2', class_='hp__hotel-name').text.strip()
    print(title)
    address = soup.find('span', class_='hp_address_subtitle').text.strip()
    print(address)
    reviews = soup.find('div', class_='_6a1b6ff88e').text.strip()
    print(reviews)
    rating = soup.find('div', class_='e5a32fd86b').text.strip()
    print(rating)

    table = soup.find('table', class_="hprt-table")

    for facility_temp in table.find_all('div', class_="hprt-facilities-facility"):
        facilities.append(facility_temp.span.text.strip())
    for facility in table.find_all('span', class_="hprt-facilities-facility"):
        facilities.append(facility.text.strip())
    print(facilities)
    for row in table.find_all('tr', class_="js-rt-block-row"):
        #RoomType = table.find('a', class_="hprt-roomtype-link").span.text.strip()
        RoomId = row.attrs['data-block-id'].rsplit('_', 4)[0]
        #firstRoomId = table.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
        print("Room Id:",RoomId)
        for firstcell in row.find_all('td', class_="-first"):
            firstR = firstcell.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
            RoomType = firstcell.find('a', class_="hprt-roomtype-link").span.text.strip()
        #print(firstR)
        if(firstR == RoomId):
            print("Room Type :",RoomType)

        Sleeps = row.find('span', class_="bui-u-sr-only").text.strip()
        print("Sleeps :",Sleeps)
        Price = row.find('span', class_="prco-valign-middle-helper").text.strip()
        print("Price :",Price)
        Choices_temp = row.find('ul', class_="hprt-conditions").text
        Choices = " ".join(Choices_temp.split())
        print("Choices :",Choices)
        Select = row.find('select', class_="hprt-nos-select")
        options = []
        for option in Select.find_all('option'):
            #print(option.text.strip())
            options.append(option.text.strip().replace("\n\xa0\n\xa0\xa0\xa0\n"," ").replace("\xa0",""))
        Rooms = options[1:]
        print("Price per Room :", Rooms)
        print("")
    ul = soup.find('ul', class_="v2_review-scores__subscore__inner")
    for li in ul.find_all('li', class_="v2_review-scores__subscore"):
        score_title = li.find('span', class_="c-score-bar__title").text.strip()
        score_bar = li.find('span', class_="c-score-bar__score").text.strip()
        scores.append(score_title +" : "+ score_bar)
    print("Scores :", scores)
    print("")

    checkin = soup.find('a', class_="av-summary-checkin").text.strip()
    checkout = soup.find('a', class_="av-summary-checkout").text.strip()
    print("Check In Date :",checkin)
    print("Check out Date :",checkout)
    i = i+1
