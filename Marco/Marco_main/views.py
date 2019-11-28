from django.shortcuts import render
from django.http import HttpResponse, JsonResponse# Create your views here.
from django.views import View
from django.views import generic

class Marco_main(generic.TemplateView) :
    template_name = 'marco_main/main_view.html'
    def get(self, request, *args, **kwargs):
        my_Sensor = '1111'
        return render(request, self.template_name, { 'Sensor' : my_Sensor})

    def post(self, request, *args, **kwargs):
        #센서 ON

        #센서 off

        image_url = 'static/gif/testimg3.gif'
        image_src = "http://127.0.0.1:8000/" + image_url
        text_content = "안녕하세요 ㅎㅎㅎ"
        data = {'Image': image_url, 'src': image_src, 'text': text_content}
        return JsonResponse(data)


    #if request.method == "POST":


