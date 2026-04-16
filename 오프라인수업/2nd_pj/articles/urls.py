from django.contrib import admin
from django.urls import path
from . import views

# 다른 앱과 혼동하지 않기 위해서
# url naming pattern에 사용
app_name = 'articles'
number = 1
urlpatterns = [
    # views.py의 index 함수를 실행하겠다.
    # html에서 href = "index/" 이런식으로 url을 하드코딩하지 않는다.
    # name = 'index' -> named url patterns
    # {% url 'articles:index' % }
    path('index/', views.index, name = 'index'),
    path('dinner/', views.dinner, name = 'dinner'),
    path('search/', views.search, name = 'search'),
    path('throw/', views.throw, name ="throw"),
    path('catch/', views.catch, name ="catch"),
    # <데이터타입 : 변수명> : 여러개의 url(숫자만 다른)을 하나의 뷰로 처리
    # variable routing
    path('<int:number>/', views.detail, name = 'detail'),
]