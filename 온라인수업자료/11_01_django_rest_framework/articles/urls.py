from django.urls import path
from articles import views

urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_id>/', views.article_detail),
    path('comments/', views.comment_list),
    path('comments/<int:comment_id>/', views.comment_detail),
    path('articles/<int:article_id>/comments/', views.comment_create),
]
