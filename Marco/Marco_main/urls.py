from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Marco_main'

urlpatterns = [
    url('api-auth/', views.Marco_main.as_view(), name='Marco'),
    url(r'^$', views.Marco_main.as_view(), name='Marco'),
    #url(r'^todo_list/$', views.Todo_subject_restful_main.as_view(), name='todo_list'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)