from django.urls import path

from . import views

app_name = 'articles'

urlpatterns = [
    # 홈페이지(전체 게시글 조회) - CRUD 중에 Read
    path('', views.index, name = 'index'),
    # variable routing
    path('<int:pk>/', views.detail, name = 'detail'),
    # 왜 url을 2개로 나눴을까?
    # 페이지 렌더링
    path('new/', views.new, name = 'new'),
    # 페이지 리다이렉트
    path('create/', views.create, name =  'create'),
    # 페이지 렌더링
    path('<int:pk>/edit/', views.edit, name = 'edit'),
    # 페이저 리다이렉트
    path('<int:pk>/update/', views.update, name = 'update'),

    path('<int:pk>/delete/', views.delete, name = 'delete'),
]
