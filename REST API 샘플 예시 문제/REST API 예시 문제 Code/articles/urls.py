from django.urls import path
from . import views


urlpatterns = [
    path('article_list/', views.article_list),
    path('articles/<article_pk>/', views.article_detail),
]
