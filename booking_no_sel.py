import requests
from bs4 import BeautifulSoup as bs
import subprocess
import pymongo
from pymongo import MongoClient
import numpy as np
import re
# from requests.exceptions import ConnectionError
# import time
import socket


links = []
i = 0
headers = []
facilities = []
scores = []
rooms = []
sleeps = []
hotel = []
record1 = { "appliance":"fan",
           "quantity":10,
           "rating":"3 stars",
           "company":"havells"}
#db
cluster = MongoClient("mongodb+srv://Vasiloudis:Vasiloudis@myCluster.bjuk6.mongodb.net/booking?ssl=true&ssl_cert_reqs=CERT_NONE")
my_db = cluster["booking"]
my_collection = my_db["hotels"]
# test = {"id": 0, "name": "a Name", "age": 25}
# my_collection.insert_one(test)


#my_collection.drop() #gia delete collection


in_month = 1
in_day = 25
in_year = 2022
out_month = 1
out_day = 30
out_year = 2022
people = 2
city = "Skiathos"
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

#properties = soup.find('div', class_='sr_header--title').text.strip() if soup.find('div', class_='sr_header--title') else ""
properties = soup.find('h1', class_='_30227359d').text.strip() #if soup.find('div', class_='sr_header--title') else ""
print(properties)
number = re.sub("[^0-9]", "", properties)
print(number+" Hotels")
loopnumber = round(np.ceil(int(float(number)/25))) #vriskw ton arithmo twn selidwn gia na kanw loop oles tis selides
print(str(loopnumber+1)+" Pages")


pages = np.arange(0, loopnumber+1, 1)
#print(pages)

for page in pages:
    temp_link = link+"&rows=25&offset="+str(page*25) #"https://www.booking.com/searchresults.gr.html?checkin_month=6&checkin_monthday=25&checkin_year=2021&checkout_month=6&checkout_monthday=30&checkout_year=2021&group_adults=2&group_children=0&order=price&ss=Kastelorizo%2C%20Greece&offset=0"
    #print(temp_link)
    offset_page = requests.get(temp_link, headers = headers)
    soup = bs(offset_page.content, 'lxml')
    #ftiaxnw lista me ola ta urls twn ksenodoxeiwn
    #for a in soup.find_all('a', {'class':'hotel_name_link'}):
    for a in soup.find_all('a', {'class':'fb01724e5b'}):
        links.insert(0, a['href'].strip())
    links.reverse()
    #print(links)
#print(links)
print(str(len(links))+" urls found")

while i < len(links):
    # page = requests.get('https://booking.com'+links[i], headers = headers)
    page = requests.get(links[i], headers = headers)
    soup = bs(page.content, 'lxml')

    checkin = soup.find('a', class_="av-summary-checkin").text.strip()
    checkout = soup.find('a', class_="av-summary-checkout").text.strip()
    #print("Check In Date :",checkin)
    #print("Check out Date :",checkout)
    ul = soup.find('ul', class_="v2_review-scores__subscore__inner")
    if soup.find('ul', class_="v2_review-scores__subscore__inner"):
        for li in ul.find_all('li', class_="v2_review-scores__subscore"):
            score_title = li.find('span', class_="c-score-bar__title").text.strip()
            score_bar = li.find('span', class_="c-score-bar__score").text.strip()
            scores.append(score_title +" : "+ score_bar)
        #print("Scores :", scores)

    else:
        #print("No Scores found")
        scores = []
    #print("")

    hotel_id = soup.find('p', class_='hp-lists-counter').attrs['data-hotel-id'].strip()
    #print("Hotel ID :"+ hotel_id)
    img_link = soup.find('img', class_='hide').attrs['src']
    #print("Image link :"+img_link)
    hotel_link = links[i]
    #print("Hotel link :"+ hotel_link)
    name = soup.find('h2', class_='hp__hotel-name').text.strip()
    #print(name)
    address = soup.find('span', class_='hp_address_subtitle').text.strip()
    #print(address)
    reviews = soup.find('div', class_='_6a1b6ff88e').text.strip() if soup.find('div', class_='_6a1b6ff88e') else "0 reviews"
    #print(reviews)
    rating = soup.find('div', class_='e5a32fd86b').text.strip() if soup.find('div', class_='e5a32fd86b') else "None"
    #print(rating)
    #print("")


    table = soup.find('table', class_="hprt-table")

    for row in table.find_all('tr', class_="js-rt-block-row"):
        # facilities = []
        #RoomType = table.find('a', class_="hprt-roomtype-link").span.text.strip()
        roomId = row.attrs['data-block-id'].rsplit('_', 4)[0]
        #firstRoomId = table.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
        #print("Room Id:",roomId)

        for firstcell in row.find_all('td', class_="-first"):
            firstR = firstcell.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
            roomType = firstcell.find('a', class_="hprt-roomtype-link").span.text.strip()

        for facility_temp in row.find_all('div', class_="hprt-facilities-facility"):
            facilities.append(facility_temp.span.text.strip())
        for facility in row.find_all('span', class_="hprt-facilities-facility"):
            facilities.append(facility.text.strip())
        #print(facilities)

        #print(firstR)
        #if(firstR == roomId):
            #print("Room Type :",roomType)





        sleep = row.find('span', class_="bui-u-sr-only").text.strip()
        #print("Sleeps :",sleep)
        price = row.find('span', class_="prco-valign-middle-helper").text.strip()
        #print("Price :",price)
        #choices_temp = row.find('ul', class_="hprt-conditions-bui").text if soup.find('ul', class_="hprt-conditions-bui") else "no Choices"
        choices_temp = row.find('td', class_="hprt-table-cell-conditions").text
        choices = " ".join(choices_temp.split())
        #print(choices)
        #print("Choices :",choices)
        select = row.find('select', class_="hprt-nos-select")
        options = []
        for option in select.find_all('option'):
            #print(option.text.strip())
            options.append(option.text.strip().replace("\n\xa0\n\xa0\xa0\xa0\n"," ").replace("\xa0",""))
        price_per_room = options[1:]
        #print("Price per Room :", price_per_room)
        sleeps = [ {"persons": sleep, "price": price, "choices": choices," price_per_room": price_per_room} ]

        rooms += [ {"id": roomId, "type": roomType,"facilities": facilities, "sleeps": sleeps}]
        facilities = []

        #print(sleeps)
        # for facility_temp in row.find_all('div', class_="hprt-facilities-facility"):
        #     facilities.append(facility_temp.span.text.strip())
        # for facility in row.find_all('span', class_="hprt-facilities-facility"):
        #     facilities.append(facility.text.strip())
        # print(facilities)
        # facilities = []


    #print("----------------------------------------------------------------------------------------")




    #sleeps = [ {"persons": sleep, "price": price, "choices": choices,"facilities": facilities," price_per_room": price_per_room} ]
    #rooms = [ {"id": roomId, "type": roomType, "sleeps": sleeps}]
    hotel = {"id":hotel_id, "link": hotel_link, "icon": img_link, "name": name, "address": address, "reviews": reviews, "rating": rating, "rooms": rooms}
    #print(hotel)
    #my_collection.update_one({"check_in": checkin,"check_out": checkout},{ "$set": { "scores": scores, "hotel": hotel} }, True)
    #my_collection.insert({"check_in": checkin,"check_out": checkout,"scores": scores, "hotel": hotel}) #insert doulevei


    my_collection.update_one({'key':hotel_id},{"$set": {"check_in": checkin,"check_out": checkout,"scores": scores, "hotel": hotel}}, True)
    rooms = []
    sleeps = []
    scores = []
    facilities = []
    i = i+1
