#lxml ,beatifulsoup4, requests 필요함 #geopy 필요함
#pprint(html.text)
#haversine 필요함
##네이버 날씨 크롤링
from haversine import haversine
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests
html = requests.get('https://search.naver.com/search.naver?query=날씨')
soup = bs(html.text,'html.parser')
location = soup.find("h2", {'class': "title"}).text # 주소 정보
temperature = soup.find("div", {'class': "temperature_text"}).text.strip()[5:]
weather = soup.find("span", {'class': "weather before_slash"}).text
air = soup.find("ul", {'class': 'today_chart_list'}).text.strip()
pprint(location)
pprint(temperature)
pprint(weather)
pprint(air)

## 현재 위치 위도 경도 가져옴
# OpenStreetMap에서 제공하는 Nominatim API를 이용하여 GPS 정보를 가져옴
response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": location, "format": "json"})

if response.status_code == 200 and len(response.json()) > 0:
    data = response.json()[0]
    latitude = float(data["lat"])
    longitude = float(data["lon"])
    print("위도:", latitude)
    print("경도:", longitude)
else:
    print("GPS 정보를 가져올 수 없습니다.")
GPS=(latitude,longitude)
print(GPS)

def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)
    return address
address = geocoding_reverse(GPS)
print(address)
address_parts = address[0].split(", ")
matching_part = None
for part in address_parts:
    if "시" in part:
        matching_part = part
        break
for part in address_parts:
    if "군" in part:
        matching_part = part
        break
if '서울' in address_parts:
	matching_part='서울'
if '대전' in address_parts:
	matching_part='대전'
if '광주' in address_parts:
	matching_part='광주'
if '울산' in address_parts:
	matching_part='울산'
if '부산' in address_parts:
	matching_part='부산'
if '세종' in address_parts:
	matching_part='세종'
if '대구' in address_parts:
    matching_part = '대구'

print(matching_part)
##광역시는 그냥 도시 이름이 나옴 대전 서울 세종, 시는 그냥나옴 군도 그냥나옴
#pandas,openpyxl
import pandas as pd
walk = pd.read_excel("C:/Users/ericr/Desktop/qtrail.xlsx")
print(walk)

a = matching_part
int_line = walk['SIGNGU_NM'].str.contains(a)
save_int_line = walk[int_line]
print(save_int_line)

print("원하는 장소를 입력해주세요")
b=input()
zero_line = walk['WLK_COURS_FLAG_NM'].str.contains(b)
s_int_line = walk[zero_line]
print (s_int_line)

row_index = walk[walk.eq(b).any(axis=1)].index[0]
column_index=14
Latitude=walk.iloc[row_index,column_index]
column_index=15
Longitude=walk.iloc[row_index,column_index]

#Latitude, Longitude
walkplace = (Latitude, Longitude)

# 거리 계산
distance=haversine(GPS, walkplace, unit = 'km')
print(distance)