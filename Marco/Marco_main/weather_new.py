from urllib.request import urlopen, Request
import urllib
import bs4
import ssl

c1, c2 = 0, 0

def current_weather(html):
    if c2==0 :
        c1 = 1
        '''
        location = '청주'
        enc_location = urllib.parse.quote(location + '+날씨')
        context = ssl._create_unverified_context()

        url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

        req = Request(url)
    
        page = urlopen(req, context=context)
        html = page.read()
        '''
        soup = bs4.BeautifulSoup(html,'html.parser')
        weather = soup.find('ul', class_='info_list').find('p', class_='cast_txt').text
        if weather.split(',')[0] == '구름 조금' or '흐림' or '안개' or '흐려짐' or '구름 많음':
            weather = '흐림'
        elif weather.split(',')[0]('갬') == True:
            weather = '흐림'
        elif weather.split(',')[0] == '비' or '진눈깨비' or '소나기' or '뇌우' or '흐려져 뇌우' or '흐려져 비' or '흐려져 진눈깨비':
            weather = '비'
        elif weather.split(',')[0] == '눈' or '소낙 눈' or '흐려져 눈':
            weather = '눈'
        else:
            weather = weather.split(',')[0]
        out_temp = soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text
        #현재 온도 출력
        #print('현재 ' + location + ' 온도는 ' + soup.find('p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.')
        str1 = soup.find('ul', class_='info_list').find('p', class_='cast_txt').text
        c1 = 0
        return (weather, out_temp, str1)
        #print(weather)
    
def daily_weather(html):
    if c1==0 :
        c2 = 1
        '''
        location = '청주'
        enc_location = urllib.parse.quote(location + '+날씨')
        context = ssl._create_unverified_context()

        url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location
        
        req = Request(url)
        page = urlopen(req, context=context)
        html = page.read()
        '''
        soup = bs4.BeautifulSoup(html,'html.parser')
        rain_flag = 0
        today_weather_list = soup.find('ul', class_="list_area").find_all('li', limit = 8)
        for i in today_weather_list:
            weather_list = i.find('dl').find_all('dd', limit = 3)
            for j in weather_list:
                if j.text == '비' or '진눈깨비' or '소나기' or '뇌우' or '흐려져 뇌우' or '흐려져 비' or '흐려져 진눈깨비':
                    rain_flag = 1
            #오늘 비가 오는 지 확인
        c2 = 0
        return rain_flag
#current_weather()
