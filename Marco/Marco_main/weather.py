from urllib.request import urlopen, Request
import urllib
import bs4
import ssl

context = ssl._create_unverified_context()

location = '청주'
enc_location = urllib.parse.quote(location + '+날씨')

url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location
try :
    req = Request(url)
    page = urlopen(req, context=context)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'html.parser')
except :
    pass
def current_weather():

    #날씨 및 어제와의 차이
    str1 = soup.find('ul', class_='info_list').find('p', class_='cast_txt').text
    #현재 온도 출력
    print(soup.find('ul', class_='info_list'))
    #print('현재 ' + location + ' 온도는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '입니다.')
    return (str1, soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text)
def daily_weather():
    
    temper = None
    weather = None
    time = None

    today_weather_list = soup.find('ul', class_="list_area").find_all('li', limit = 8)
    weatherlist = []
    for i in today_weather_list:
        flag = 0
        weather_list = i.find('dl').find_all('dd', limit = 3)
        for j in weather_list:
            if flag == 0:
                temper = j.find('span').text
                flag += 1
            elif flag == 1:
                weather = j.text
                flag += 1
            else:
                time = j.text
        #현재 시간부터의 날씨, 온도 출력
        weatherlist.append((time.replace(" ", ""), weather, temper.replace(" ", "")))
    return weatherlist
