import RPi.GPIO as GPIO
import time
import Adafruit_DHT as dht
import picamera
from pyowm import OWM
import datetime
import os

def Camera_function(cnt):
    camera = picamera.PiCamera()
    #camera.start_preview()
    time.sleep(2)
    #camera.capture('image.jpg')
    filename = "static/video/"+str(cnt)+".h264"
    filename2 = "static/video/"+str(cnt)+".mp4"
    camera.start_recording(filename)
    time.sleep(7)
    camera.stop_recording()
    camera.close()
    #camera.stop_preview()
    MP4Box="MP4Box -add "+filename+" "+filename2
    deleteh264 = "rm "+filename
    print(MP4Box)
    os.system(MP4Box)
    os.system(deleteh264)
    time.sleep(2)
    return filename2

def Temper_function() :
    h, t = dht.read_retry(dht.DHT11, 4)
    return (str(t), str(h))

def Weather_function():
    API_key = 'cf1b1afad4e36a051b4a369d3cc3ed3f'
    owm = OWM(API_key)
    obs = owm.weather_at_place('Cheongju') # current weather
    ob = obs.get_weather()
    nowWeather= (ob.get_status(), ob.get_temperature(unit='celsius')['temp'])
    #print(ob.get_status(), ob.get_temperature(unit='celsius')['temp'])
    forecaster = owm.three_hours_forecast('Cheongju')
    #forecaster = owm.daily_forecast('Cheongju')
    f = forecaster.get_forecast()
    now = datetime.datetime.now()# - datetime.timedelta(days=0, hours=9) is utc
    weatherlist = []
    rain_flag = False
    for weather in f : #
        w = weather.get_reference_time('date')+datetime.timedelta(hours=9)
        
        if (w.day == now.day and \
            w.hour > now.hour) or \
           w.day -1 == now.day or \
            (now.day >=28 and w.day < 2) :
            if w.day == now.day and weather.get_status() =="Clouds" :
                rain_flag = True
            weatherlist.append((w, weather.get_status(), weather.get_temperature(unit='celsius')['temp']))
            #print(w, weather.get_status(), weather.get_temperature(unit='celsius')['temp'])
    
    return (nowWeather,weatherlist,rain_flag)
    #time = datetime.datetime.now() #+ datetime.timedelta(days=0, hours=9)
    #KST = datetime.timezone(datetime.timedelta(hours=9)) # timezone 설정변수 UTC+9 
    #time02 = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second, tzinfo=datetime.timezone.utc)
    #print(time02)
    #print(time)
    #print(time02)
    #w = forecaster.get_weather_at(time02)
    #temperature = w.get_temperature(unit='celsius')['temp']
    #temperature = (temperature-32) * 1.8
    #print(w.get_status(), temperature)
    #w = obs.get_weather()
    # clouds, clear, atmosphere, snow, rain, drizzle, thunderstorm
    # print ('Cheongju :', w.get_status(), w.get_temperature(unit='celsius')['temp'])
    
    #return (w.get_status(), str(w.get_temperature(unit='celsius')['temp']))

def IR_sensor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.IN)
    A = GPIO.input(16)
    #time.sleep(1)
    #B = GPIO.input(16)
    return (not A)# and (not B)
Weather_function()
