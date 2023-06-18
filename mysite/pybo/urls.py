from django.urls import path
from . import views
#from django.contrib.staticfiles.urls import static
#import accounts.views

app_name = 'pybo'

urlpatterns = [
    #시작 화면 및 로그인
    path('start/', views.web_start, name='start'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #사용자 정보 출력
    path('loca/', views.user_location, name='location'),
    #장소 리스트 출력
    path('cinfo/', views.cinfo, name='cafeinfo'),
    path('ainfo/', views.ainfo, name='artinfo'),
    path('tinfo/', views.tinfo, name='info'),
    #장소 결과 출력
    path('cresult/', views.get_cafe_info, name='cafeweather'),
    path('aresult/', views.get_art_info, name='artweather'),
    path('tresult/', views.weather_view, name='weather_view'),
    #제작자 페이지
    path('maker/', views.maker, name='maker'),
    path('gil/', views.gil ,name='gil'),
    path('rak/', views.rak ,name='rak'),
    path('min/', views.min ,name='min'),
    path('jun/', views.jun ,name='jun'),
    #제작자 개인연락처 페이지
    path('rak/contact/', views.rakcontact, name='rakcontact'),
    path('gil/contact/', views.gilcontact, name='gilcontact'),
    path('jun/contact/', views.juncontact, name='juncontact'),
    path('min/contact/', views.mincontact, name='mincontact'),
    #이스터에그
    path('dandaegi/', views.dandaegi, name='dandaegi'),

    #path('start/sec1/', views.user_sec1, name='section1'),
    #path('weather/<str:address>/', views.weather_view, name='weather_view'),
]
