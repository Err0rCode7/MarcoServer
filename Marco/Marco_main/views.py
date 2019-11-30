from django.shortcuts import render
from django.http import HttpResponse, JsonResponse# Create your views here.
from django.views import View
from django.views import generic
from . import sensor, calendar, drive, soundoutput
from datetime import datetime
import time

#import threading





def initiallizing() :
    global in_temper, humidity, rain_flag
    global dayweather, weather_text, out_temper
    in_temper, humidity = sensor.Temper_function()
    now_w, weatherList, rain_flag = sensor.Weather_function()
    dayweather, out_temper = now_w[0], str(now_w[1])
    if rain_flag :
        weather_text = "날씨: "+dayweather + ", 비소식이 있어요"
    else :
        weather_text = "날씨: "+dayweather


in_temper, humidity, lock, driveflag= 0, 0, 0, 0
dayweather, out_stemper, weather_text = 0, 0, 0
filename, soundfile, soundcnt = "", "", 0
initiallizing()

class Marco_main(generic.TemplateView) :
    template_name = 'marco_main/main_view.html'
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        global in_temper, humidity, rain_flag
        global lock, driveflag, soundcnt
        global dayweather, weather_text, out_temper
        
        text_content = "" # 전체 대사
        temp_text = "" # 온도관련 대사
        camera = "off" # 카메라 상태
        event = False # 이벤트 발생조건
        character = 'static/character/base3.gif'
        text_ct = ""
        schedule = calendar.get_schedule()
        listofschedule = []
        if schedule:
            for x in schedule :
                str1 = x[0]+ "/" + x[1] + " " + x[2] + "시" + x[3] + "분 " + x[5]
                listofschedule.append(str1)
            for x in range(0,3-len(listofschedule)) :
                listofschedule.append("")
        else :
            listofschedule = [""] * 3
            
        now = datetime.now()
        hour, minute, second = now.hour, now.minute, now.second
        # default setting #
        
        # 3시간 간격으로 날씨, 실내 정보 업데이트 #
        if hour % 3 == 0 and minute == 0 and second < 5 :
            initiallizing()
        
        # clouds, clear, atmosphere, snow, rain, drizzle, thunderstorm            
        backimg_url = 'static/gif/clear.png'
        '''
        if dayweather == 'Clouds' : # 'weather' :
            backimg_url = 'static/gif/clouds.gif'
        elif dayweather == 'Clear' : 
            backimg_url = 'static/gif/clear.png'
        elif dayweather == 'Rain' : #'weather' :
            backimg_url = 'static/gif/rain.gif'
        elif dayweather == 'Snow' : #'weather' :
            backimg_url = 'static/gif/snow.gif'        
        else :
            backimg_url = ''
        '''
        # default setting #
        
        # 대사 : 실내 온습도 이벤트, 실외 온도 이벤트 #
        if float(out_temper) < 7 :
            temp_text = "날씨가 추워졌어요"
        elif float(out_temper) > 24 :
            pass
        if float(in_temper) < 5 :
            pass
            
        # 대사 : 실내 온습도 이벤트, 실외 온도 이벤트 #    

        # ajax message and lock off #           
        if lock == 0 and request.POST['message'] == "on" and request.POST['textlock'] == "True":
            lock = 1
            camera = "off"
            print("Camera on!!")
            #t = threading.Thread(target=sensor.Camera_function,args=now)

            filename = str(now.month)+"-" + str(now.day)+"_"+str(hour)+":"+str(minute)
            print("Filename : ",filename)
            filename = sensor.Camera_function(filename)
            driveflag, lock, soundcnt = 1, 0, 0
        # ajax message and lock off #    
        
        # google drive #
        if lock == 0 and driveflag == 1 :
            
            driveflag = 0
            print(drive.uploding_file(filename))
        # google drive #
            
           

        # IR sensing and occur event #
        if sensor.IR_sensor() :
            if soundcnt <=3 :
                soundcnt += 1
                soundfile = "static/sound/marco_alarm.wav"
                soundoutput.sound_print(soundfile)
            event = True
            #backimg_url = 'static/gif/rain.gif'
            text_content = ""#"Sensor On !!"
            camera = "on"
            character = 'static/character/char_schedule.gif'
            text_ct = 'static/textimg/text.png'
            # FCM_request #
            # pass
            # FcM_request #
        # IR sensing and occur event #
        
        backimg_src = "http://127.0.0.1:8000/" + backimg_url # 배경 핸들링 변수
        character_src = "http://127.0.0.1:8000/" + character # 캐릭터 핸들링 변수
        text_src = "http://127.0.0.1:8000/" + text_ct # 캐릭터 핸들링 변수

        data = {'Backimg': backimg_url, 'Backimg_src': backimg_src, 'text':text_content,
                'in_temper': in_temper+"°", 'humidity': humidity+" %", 'weather': weather_text,
                'out_temper': out_temper+"°", 'event': event, 'schedule': listofschedule,
                'camera': camera, 'character': character, 'character_src': character_src,
                'text_ct': text_ct, 'text_src': text_src }
        
        return JsonResponse(data)


