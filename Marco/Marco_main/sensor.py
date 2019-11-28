import RPi.GPIO as GPIO
import time
import Adafruit_DHT as dht
import picamera
from pyowm import OWM



def Camera_function(cnt):
    camera = picamera.PiCamera()
    #camera.start_preview()
    time.sleep(2)
    #camera.capture('image.jpg')
    camera.start_recording("static/video/"+str(cnt)+".h264")
    time.sleep(8)
    camera.stop_recording()
    camera.close()
    #camera.stop_preview()

def Temper_function() :
    h, t = dht.read_retry(dht.DHT11, 4)
    return (str(t), str(h))
    
def Weather_function():
    API_key = 'cf1b1afad4e36a051b4a369d3cc3ed3f'
    owm = OWM(API_key)
    obs = owm.weather_at_place('Cheongju')
    w = obs.get_weather()
    # clouds, clear, atmosphere, snow, rain, drizzle, thunderstorm
    # print ('Cheongju :', w.get_status(), w.get_temperature(unit='celsius')['temp'])
    return (w.get_status(), str(w.get_temperature(unit='celsius')['temp']))

def IR_sensor():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.IN)
    A = GPIO.input(16)
    #time.sleep(1)
    #B = GPIO.input(16)
    return (not A)# and (not B)