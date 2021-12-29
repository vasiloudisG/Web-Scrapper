import requests
from bs4 import BeautifulSoup as bs
import pymongo
from pymongo import MongoClient
import numpy as np
import re
from datetime import date, datetime
import random
from random import randint
import csv
# from requests.exceptions import ConnectionError
# import time


links = []
i = 0
headers = []
facilities = []
scores = []
choices = []
rooms = []
sleeps = []
hotel = []
imgs = []

#db
cluster = MongoClient("mongodb+srv://Vasiloudis:Vasiloudis@myCluster.bjuk6.mongodb.net/booking?ssl=true&ssl_cert_reqs=CERT_NONE")
my_db = cluster["booking"]
my_collection = my_db["hotels"]
basic_data = my_db["basic_data"]
basic_datas = my_db["basic_datas"]
# test = {"id": 0, "name": "a Name", "age": 25}
# my_collection.insert_one(test)


#my_collection.drop() #gia delete collection

# in_month = 1
# in_day = 20
# in_year = 2022
# out_month = 1
# out_day = 30
# out_year = 2022
# people = 1
# city = "Skiathos"
# country = "Greece"

todate = datetime.today().strftime('%Y-%m-%d')
f_date = date(my_db.basic_datas.find_one()['in_year'], my_db.basic_datas.find_one()['in_month'], my_db.basic_datas.find_one()['in_day'])
l_date = date(my_db.basic_datas.find_one()['out_year'], my_db.basic_datas.find_one()['out_month'], my_db.basic_datas.find_one()['out_day'])
# print(f_date)
# print(l_date)
total_days = l_date - f_date
#print(total_days.days)

#my_db.basic_data.insert_one({"in_year" : in_year ,"out_year" : out_year, "in_month" : in_month, "out_month" : out_month, "in_day" : in_day, "out_day" : out_day , "people" : people, "city" : city, "country" : country})

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Scraper Started at : ", current_time)

#exit()
today = int(str(date.today()).split('-')[2])
tomorrow = int(str(date.today()).split('-')[2])+1

link = "https://www.booking.com/searchresults.html?checkin_month={in_month}&checkin_monthday={in_day}" \
    "&checkin_year={in_year}&checkout_month={out_month}&checkout_monthday={out_day}&checkout_year={out_year}" \
    "&group_adults={people}&group_children=0&order=price&ss={city}%2C%20{country}" \
    ";changed_currency=1;selected_currency=EUR;top_currency=1" \
        .format(in_month=my_db.basic_datas.find_one()['in_month'],
                in_day=str(today),#my_db.basic_datas.find_one()['in_day'],
                in_year=my_db.basic_datas.find_one()['in_year'],
                out_month=my_db.basic_datas.find_one()['out_month'],
                out_day=str(tomorrow),#my_db.basic_datas.find_one()['out_day'],
                out_year=my_db.basic_datas.find_one()['out_year'],
                people=my_db.basic_datas.find_one()['people'],
                city=my_db.basic_datas.find_one()['city'],
                country=my_db.basic_datas.find_one()['country'])

print(link)
#exit()
#csv header
header = ['Date','Hotel Name','Hotel ID','Room Name','Room ID','Price']
with open('dpr/'+todate+'-Rooms.csv', 'a', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
            

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

#exit()
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
        links.insert(0, a['href'].strip()+";changed_currency=1;selected_currency=AUD;top_currency=1")
    #links.reverse()
    #print(links)

#exit()
print(str(len(links))+" urls found")
#print(links[0])
#exit()
while i < len(links):
    # page = requests.get('https://booking.com'+links[i], headers = headers)
    page = requests.get(links[i], headers = headers)
    soup = bs(page.content, 'lxml')

    #checkin = soup.find('a', class_="av-summary-checkin").text.strip()
    #checkout = soup.find('a', class_="av-summary-checkout").text.strip()
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
    random_id = randint(100000, 9999999)
    hotel_link = links[i].split('?', 1)[0]
    #print("Hotel link :"+ hotel_link)
    hotel_id = soup.find('p', class_='hp-lists-counter').attrs['data-hotel-id'].strip() if soup.find('p', class_='hp-lists-counter').attrs['data-hotel-id'] else random_id
    #print("Hotel ID :"+ hotel_id)
    img_link = soup.find('img', class_='hide').attrs['src']
    #print("Image link :"+img_link)
   
    #name = soup.find('h2', class_='hp__hotel-name').text.strip()
    #print(name)
    name_temp = soup.find('h2', class_='hp__hotel-name')
    type = name_temp.find('span', class_="bui-badge").text.strip() if name_temp.find('span', class_="bui-badge") else  name_temp.find('span', class_="hp__hotel-type-badge").text.strip()
    #print(type)
    name = str(name_temp).split("</span>")[1].split("<")[0].strip()
    if name == "" : #if its new to booking
        name = soup.find('h2', class_="hp__hotel-name").text.strip().split("\n\n")[-1].strip()
    #print(name)
    address = soup.find('span', class_='hp_address_subtitle').text.strip()
    #print(address)   
    if soup.find('div', class_='_4abc4c3d5'):
        reviews = soup.find('div', class_='_4abc4c3d5').text.strip().split()[0] 
        if ',' in reviews:
            reviews = reviews.replace(",", "")
    else:
        reviews = -1  
    #print(reviews)
    rating = soup.find('div', class_='_9c5f726ff').text.strip() if soup.find('div', class_='_9c5f726ff') else -1
    if rating != -1 and len(rating) > 5 :
        rating = rating.split()[1]
    #print(rating)
    #print("")
    photo_div = soup.find('div', class_='bh-photo-grid') 
    try:
        photo_div.find('div', class_="reviews-carousel-container").extract()
    except AttributeError:
        pass  # sometimes there is no 'reviews-carousel-container'
    for img in photo_div.find_all('img'):
        imgs.append(img['src'])
    random.shuffle(imgs)

    table = soup.find('table', class_="hprt-table")

    for row in table.find_all('tr', class_="js-rt-block-row"):
        # facilities = []
        #RoomType = table.find('a', class_="hprt-roomtype-link").span.text.strip()
        roomId = row.attrs['data-block-id'].rsplit('_', 4)[0]
        #firstRoomId = table.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
        #print("Room Id:",roomId)

        for firstcell in row.find_all('td', class_="-first"):
            #firstR = firstcell.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
            roomType = firstcell.find('a', class_="hprt-roomtype-link").span.text.strip()

        for facility_temp in row.find_all('div', class_="hprt-facilities-facility"):
            facilities.append(facility_temp.span.text.strip())
        for facility in row.find_all('span', class_="hprt-facilities-facility"):
            facilities.append(facility.text.strip())
        #print(facilities)

        #print(firstR)
        #if(firstR == roomId):
            #print("Room Type :",roomType)






        sleep_temp = row.find('span', class_="bui-u-sr-only").text.strip()
        if ('-' in sleep_temp):
            sleep = sleep_temp.split('-')[1].split('g')[0].strip()
            #print(sleep)
        else:
            sleep = sleep_temp.split(':')[1].strip()
            #print(sleep)




        #print("Sleeps :",int(sleep))

        price_temp = row.find('span', class_="prco-valign-middle-helper").text.strip()
        #print(price_temp)
        temp = re.findall(r'\d+', price_temp)
        price = list(temp)
        price = "".join(price)
        #print("".join(price))
        
        #price = price_temp.split('€')[1] 
        #if ',' in price:
           #price = price.replace(",", "")
        
        #print("Price :",price)
        # choices_temp = row.find('td', class_="hprt-table-cell-conditions").text
        # choices = " ".join(choices_temp.split())
        ul2 = row.find('td', class_="hprt-table-cell-conditions") #'ul', class_="hprt-conditions-bui" #error
        choices = []
        for li2 in ul2.find_all('li', class_="bui-list__item"):
            choice = li2.find('div', class_="bui-list__description").text.strip()
            choices.append(choice)

        #print(choices)
        #print("Choices :",choices)
        select = row.find('select', class_="hprt-nos-select")
        options = []
        for option in select.find_all('option'):
            #print(option.text.strip())
            options.append(option.text.strip().replace("\n\xa0\n\xa0\xa0\xa0\n"," ").replace("\xa0",""))
        price_per_room = options[1:]
        #print("Price per Room :", price_per_room)
        sleeps = [ {"max_persons": int(sleep), "price": int(price), "choices": choices," price_per_room": price_per_room} ]
        #print(imgs)
        rooms += [ {"id": roomId, "type": roomType,"facilities": facilities,"room_imgs":imgs, "sleeps": sleeps}]
        
        facilities = []


        data = [todate,name,hotel_id,roomType,roomId,price]
        with open('dpr/'+todate+'-Rooms.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            #writer.writerow(header)
            writer.writerow(data)
        #print(rooms)
        #print(sleeps)
        # for facility_temp in row.find_all('div', class_="hprt-facilities-facility"):
        #     facilities.append(facility_temp.span.text.strip())
        # for facility in row.find_all('span', class_="hprt-facilities-facility"):
        #     facilities.append(facility.text.strip())
        # print(facilities)
        # facilities = []
    
    #imgs.clear()
    

    #print("----------------------------------------------------------------------------------------")




    #sleeps = [ {"persons": sleep, "price": price, "choices": choices,"facilities": facilities," price_per_room": price_per_room} ]
    #rooms = [ {"id": roomId, "type": roomType, "sleeps": sleeps}]
    hotel = {"days": int(str(total_days).split(' ')[0])+1,"link": hotel_link, "icon": img_link, "name": name, "type": type, "address": address, "reviews": int(reviews), "rating": float(rating), "rooms": rooms}
    #print(hotel)
    #my_collection.update_one({"check_in": checkin,"check_out": checkout},{ "$set": { "scores": scores, "hotel": hotel} }, True)
    #my_collection.insert({"check_in": checkin,"check_out": checkout,"scores": scores, "hotel": hotel}) #insert doulevei
    
    
    my_collection.update_one({'hotel_id':int(hotel_id)},{"$set": {"scores": scores, "hotel": hotel}}, True)
    rooms = []
    sleeps = []
    scores = []
    facilities = []
    imgs.clear()
    i = i+1

end = datetime.now()
current_time = end.strftime("%H:%M:%S")
print("Scraper Finished at : ", current_time)