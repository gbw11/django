from django.shortcuts import render, redirect

# Create your views here.
# model form 이 아니라 built-in form 사용
from django.contrib.auth.forms import(
    AuthenticationForm # 로그인을 위한 폼(id, password)
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .models import User

def login(request):
    if request.method == 'POST':
        # request.POST : 사용자가 입력한 ID, Password
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # get_user() : 인증된 사용자의 객체 반환
            # 후에 signup과의 차이 => 이미 DB에 존재하는 사용자를 인증
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else: #로그인 버튼(submit 버튼)을 누리기 전
        form = AuthenticationForm() # 빈폼
    # GET요청 or 유효성 검사를 실패했다.
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    # login, logout 다 POST요청
    return redirect('articles:index')