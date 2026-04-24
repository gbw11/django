from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name ='login'),
    path('logout/', views.logout, name ='logout'),
    path('signup/', views.signup, name ='signup'), # 회원가입
    # 1. 사이트 접속 2. 로그인 3. 내정보에서 회원탈퇴
    path('delete/', views.delete, name = 'delete'), # 회원 탈퇴
    path('update/', views.update, name ='update'), # 회원정보 수정
    path('password/', views.change_password, name='change_password'),
]
