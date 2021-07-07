import requests
from bs4 import BeautifulSoup as bs

i = 0
j = 0
bed_types =[]
persons = []
prices = []
facilities = []
scores = []

link = "https://www.booking.com/hotel/gr/mandraki-village-boutique.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaFyIAQGYATG4ARfIAQzYAQPoAQH4AQKIAgGoAgO4AvLV-4YGwAIB0gIkNWJiNjVhMWUtZTIyOC00Y2Q0LWEyYzMtNzkzNTAyYTQwNmI42AIE4AIB;sid=c675e9dc1cce5d36b3a4404de636530e;all_sr_blocks=1656701_329702281_0_41_0&checkin=2021-07-25&checkout=2021-07-30&dest_id=2891&dest_type=region&dist=0&group_adults=2&group_children=0&hapos=1&highlighted_blocks=1656701_329702281_0_41_0&hpos=1&no_rooms=1&sb_price_type=total&sr_order=popularity&sr_pri_blocks=1656701_329702281_0_41_0__100500&srepoch=1625223173&srpvid=c80d4c827c0a01c3&type=total&ucfs=1&#hotelTmpl"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"}

response = requests.get(link, headers = header)
soup = bs(response.content, 'lxml')

title = soup.find('h2', class_='hp__hotel-name').text.strip()
print(title)

headers = []
table = soup.find('table', class_="hprt-table")
# for i in table1.find_all('th'):
#     header = i.text.strip()
#     headers.append(header)
# print(headers)
# table2 = soup.find('th', class_="hprt-table-header-cell")
# print(table2)

#firstRoomId = table.find('a', class_="hprt-roomtype-link").attrs['data-room-id']
#print(firstRoomId)

# RoomType = table.find('a', class_="hprt-roomtype-link").span.text.strip()
# print(RoomType)
facilitiesZ = table.find('div', class_="hprt-facilities-block").text.replace("\n\n\n\n", "")
#print(facilitiesZ)
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
