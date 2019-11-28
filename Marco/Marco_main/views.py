from django.shortcuts import render
from django.http import HttpResponse, JsonResponse# Create your views here.
from django.views import View
from django.views import generic
from . import sensor
from datetime import datetime
#import threading

in_temper, humidity = sensor.Temper_function()
weather_status, out_temper = sensor.Weather_function()
cnt, lock = 0, 0

class Marco_main(generic.TemplateView) :
    template_name = 'marco_main/main_view.html'
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        global in_temper, humidity, lock
        global weather_status, out_temper, cnt
        
        #센서 ON
        print()
        # clouds, clear, atmosphere, snow, rain, drizzle, thunderstorm
        text_content = ""
        temp_text = ""
        camera = "off"
        THT = "내부 온도: "+in_temper+"" + "내부 습도: " + humidity+ ""+ "외부 습도: "+out_temper
        event = False


        if float(out_temper) < 5 :
            temp_text = "날씨가 추워졌어요"
        elif float(out_temper) > 28 :
            pass
        
        now = datetime.now()
        nowhour = now.hour
        nowminute = now.minute
        nowsecond = now.second
        if nowhour % 2 == 0 and nowminute == 0 and (nowsecond < 5):
            in_temper, humidity = sensor.Temper_function()
            weather_status, out_temper = sensor.Weather_function()
        if weather_status == 'Clouds' : #'weather' :
            backimg_url = 'static/gif/clouds.gif'
        elif weather_status == 'Clear' : #'weather' :
            backimg_url = 'static/gif/clear.gif'
        elif weather_status == 'Rain' : #'weather' :
            backimg_url = 'static/gif/rain.gif'
            


        # ajax message and lock off            
        if lock == 0 and request.POST['message'] == "on" and request.POST['textlock'] == "True":
            lock = 1
            camera = "off"
            print("Camera on!!")
            #t = threading.Thread(target=sensor.Camera_function,args=now)
            sensor.Camera_function(now)
            lock = 0
        if sensor.IR_sensor() :
            event = True
            #backimg_url = 'static/gif/rain.gif'
            text_content = "Sensor On !!"
            camera = "on"
            
        backimg_src = "http://127.0.0.1:8000/" + backimg_url
        data = {'Backimg': backimg_url, 'Backimg_src': backimg_src, 'text':text_content,
                'in_temper': in_temper, 'humidity': humidity, 'weather': weather_status,
                'out_temper': out_temper, 'event': event, 'THT': THT,'schedule': "",
                'camera': camera }
        
        return JsonResponse(data)


    #if request.method == "POST":


