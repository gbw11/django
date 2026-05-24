from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('analyze/', views.analyze, name='analyze'),
    path('profile/', views.save_profile, name='save_profile'),
]