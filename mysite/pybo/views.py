from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login
from haversine import haversine
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup as bs
import os
import requests
import pandas as pd
from django.shortcuts import render
import subprocess
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent='South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)
    return address


def user_sec1(request):
    print("나는 집에 가고 싶다")
    return render(request, 'pybo/maker.html')


def cinfo(request):
    file_path = os.path.join(BASE_DIR, 'excel', 'opsw2.xlsx')
    walk = pd.read_excel(file_path)
    int_line = walk['address'].str.contains('청주시')
    save_int_line = walk[int_line]
    results = [result[0] for result in save_int_line.values.tolist()]
    print(results)
    return render(request, 'pybo/cinfo.html', {'results': results})

def ainfo(request):
    file_path = os.path.join(BASE_DIR, 'excel', 'opsw3.xlsx')
    walk = pd.read_excel(file_path)
    int_line = walk['address'].str.contains('청주시')
    save_int_line = walk[int_line]
    results = [result[0] for result in save_int_line.values.tolist()]
    print(results)
    return render(request, 'pybo/ainfo.html', {'results': results})



def tinfo(request):
    file_path = os.path.join(BASE_DIR, 'excel', 'opsw1.xlsx')
    walk = pd.read_excel(file_path)
    int_line = walk['address'].str.contains('청주시')
    save_int_line = walk[int_line]
    results = save_int_line.values.tolist()
    results = [item[1] for item in save_int_line.values.tolist()]

    print(results)
    return render(request, 'pybo/tinfo.html', {'results': results})


def web_start(request):
   return render(request, 'pybo/start.html')

# def web_start(request):
#     print(request.method)
#     if request.method == 'POST':
#         # number.txt 파일에서 현재 숫자 읽기
#         with open('C:/Users/Maybes/Desktop/number.txt', 'r') as f:
#             current_number = int(f.read())
#             print(current_number)
#         # 숫자 증가
#         current_number += 1
#
#         # number.txt 파일에 증가된 숫자 저장
#         with open('C:/Users/Maybes/Desktop/number.txt', 'w') as f:
#             f.write(str(current_number))
#
#         # number.txt 파일에서 현재 숫자 읽기
#     with open("C:/Users/Maybes/Desktop/number.txt", 'r') as f:
#         current_number = int(f.read())
#
#         # 템플릿에 전달할 context 설정
#     context = {'current_number': current_number}
#
#     return render(request, 'pybo/start12.html', context)


def user_location(request):
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')
    location = soup.find("h2", {'class': "title"}).text  # 주소 정보
    temperature = soup.find("div", {'class': "temperature_text"}).text.strip()[5:]
    weather = soup.find("span", {'class': "weather before_slash"}).text
    air = soup.find("ul", {'class': 'today_chart_list'}).text.strip()
    # pprint(location)
    # pprint(temperature)
    # pprint(weather)
    # pprint(air)
    # response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": location, "format": "json"})
    return render(request, 'pybo/location.html',
                  {'loca3': location, 'temp3': temperature, 'weat3': weather, 'air3': air})


def weather_view(request):
    result = request.POST.get('name')
    #result='상당산성길'
    print(result)
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')
    location = soup.find("h2", {'class': "title"}).text  # 주소 정보
    response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": location, "format": "json"})

    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        latitude = float(data["lat"])
        longitude = float(data["lon"])
        print("위도:", latitude)
        print("경도:", longitude)

    GPS = (latitude, longitude)
    # print(GPS)
    address = geocoding_reverse(GPS)
    address_parts = address[0].split(", ")
    file_path = os.path.join(BASE_DIR, 'excel', 'opsw1.xlsx')
    walk = pd.read_excel(file_path)
    row_index = walk[walk.eq(result).any(axis=1)].index[0]
    place = walk.iloc[row_index, 4]
    column_index = 14
    Latitude = walk.iloc[row_index, column_index]
    column_index = 15
    Longitude = walk.iloc[row_index, column_index]

    walkplace = (Latitude, Longitude)
    distance = haversine(GPS, walkplace, unit='km')
    html = requests.get(f'https://search.naver.com/search.naver?query={place}날씨')
    soup = bs(html.text, 'html.parser')
    location2 = soup.find("h2", {'class': "title"}).text # 주소 정보
    #location2 = soup2.find("span", {'class': "btn_select"}).text.strip()
    temperature2 = soup.find("div", {'class': "temperature_text"}).text.strip()[5:]
    weather2 = soup.find("span", {'class': "weather before_slash"}).text
    air2 = soup.find("ul", {'class': 'today_chart_list'}).text.strip()
    # pprint(location2)
    # pprint(temperature2)
    # pprint(weather2)
    # pprint(air2)

    return render(request, 'pybo/tresult.html',
                  {'dist': round(distance, 2), 'name': result, 'weat': weather2, 'air': air2, 'temp': temperature2})

def get_art_info(request):
    place = request.POST.get('name')
    print(place)
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')
    location = soup.find("h2", class_="title").text  # Address information
    response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": location, "format": "json"})

    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        latitude = float(data["lat"])
        longitude = float(data["lon"])
        GPS = (latitude, longitude)

    html = requests.get(f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={place}청주')

    soup = bs(html.text, 'html.parser')
    phonenumber = soup.find("span", class_="xlx7Q").text.strip()  # Phone number
    cafeaddress = soup.find("span", class_="LDgIH").text.strip().split()[:5]
    cafeaddress = ' '.join(cafeaddress)
    print(cafeaddress)
    try:
        opentime = soup.find("span", class_="U7pYf").text.strip()[:12]
    except AttributeError:
        opentime = "10시에 운영 시작"

    caferesponse = requests.get("https://nominatim.openstreetmap.org/search",
                                params={"q": cafeaddress, "format": "json"})
    cafelatitude = 36.5853201
    cafelongitude = 127.5080576
    if caferesponse.status_code == 200 and len(caferesponse.json()) > 0:
        data = caferesponse.json()[0]
        cafelatitude = float(data["lat"])
        cafelongitude = float(data["lon"])

    print(cafelatitude, cafelongitude)
    cafegps = (cafelatitude, cafelongitude)
    distance = haversine(GPS, cafegps, unit='km')

    return render(request, 'pybo/aresult.html',
                  {'name': place, 'phonenumber': phonenumber, 'cafeaddress': cafeaddress, 'opentime': opentime,
                   'distance': round(distance, 3)})

def get_cafe_info(request):
    place = request.POST.get('name')
    print(place)
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')
    location = soup.find("h2", class_="title").text  # Address information
    response = requests.get("https://nominatim.openstreetmap.org/search", params={"q": location, "format": "json"})

    if response.status_code == 200 and len(response.json()) > 0:
        data = response.json()[0]
        latitude = float(data["lat"])
        longitude = float(data["lon"])
        GPS = (latitude, longitude)

    html = requests.get(f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={place}청주')

    soup = bs(html.text, 'html.parser')
    phonenumber = soup.find("span", class_="xlx7Q").text.strip()  # Phone number
    cafeaddress = soup.find("span", class_="LDgIH").text.strip().split()[:5]
    cafeaddress = ' '.join(cafeaddress)
    print(cafeaddress)
    try:
        opentime = soup.find("span", class_="U7pYf").text.strip()[:12]
    except AttributeError:
        opentime = "10시에 운영 시작"

    caferesponse = requests.get("https://nominatim.openstreetmap.org/search",
                                params={"q": cafeaddress, "format": "json"})
    cafelatitude = 36.5853201
    cafelongitude = 127.5080576
    if caferesponse.status_code == 200 and len(caferesponse.json()) > 0:
        data = caferesponse.json()[0]
        cafelatitude = float(data["lat"])
        cafelongitude = float(data["lon"])

    print(cafelatitude, cafelongitude)
    cafegps = (cafelatitude, cafelongitude)
    distance = haversine(GPS, cafegps, unit='km')

    return render(request, 'pybo/cresult.html',
                  {'name': place, 'phonenumber': phonenumber, 'cafeaddress': cafeaddress, 'opentime': opentime,
                   'distance': round(distance, 3)})


def maker(request):
    return render(request, 'maker/maker.html', )

def gil(request):
    return render(request, 'maker/gil.html')


def rak(request):
    return render(request, 'maker/rak.html')


def min(request):
    return render(request, 'maker/min.html')


def jun(request):
    return render(request, 'maker/jun.html')


def rakcontact(request):
    return render(request, 'maker/rakcontact.html')


def gilcontact(request):
    return render(request, 'maker/gilcontact.html')


def juncontact(request):
    return render(request, 'maker/juncontact.html')


def mincontact(request):
    return render(request, 'maker/mincontact.html')


def dandaegi(request):
    return render(request, 'maker/dandaegi.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 성공 후 리디렉션할 URL을 여기에 입력합니다.
            return redirect('pybo/loca')
        else:
            return render(request, 'pybo/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'pybo/login.html')

def register_view(request):
    if request.method == 'POST':
        # 회원가입 로직을 처리하는 코드를 여기에 작성합니다.
        # 새로운 사용자를 생성하고 저장하는 등의 작업을 수행합니다.
        return redirect('login')
    else:
        return render(request, 'pybo/register.html')

