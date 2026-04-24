from django.shortcuts import render, redirect

# Create your views here.
# model form 이 아니라 built-in form 사용
from django.contrib.auth.forms import(
    AuthenticationForm, # 로그인을 위한 폼(id, password)
    PasswordChangeForm # 비밀번호 변경 폼(현재 비밀번호, 변경할 비밀번호)
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .models import User

from django.contrib.auth.decorators import login_required

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

@login_required
def logout(request):
    auth_logout(request)
    # login, logout 다 POST요청
    return redirect('articles:index')

from .forms import CustomUserCreationForm, CustomUserChangeForm

def signup(request):
    # is_authenticated : 이미 인증된 사용자라면
    # 상황 : 이미 로그인하고, 회원가입 페이지로 이동하려고 할 때
    if request.user.is_authenticated:
        return redirect('articles:index')
    
    # 필수 입력 다하고, 회원가입 완료 버튼 눌렀을 때
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid(): # 1. 유효성 검사
            user = form.save() # 2. DB에 저장
            auth_login(request, user) # 3. 로그인
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    
    context={
        'form' : form
    }

    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    # request.user : 현재 로그인 되어 있는 user의 정보
    request.user.delete()
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == "POST":
        # request.POST : 내가 입력한 필드의 값
        # instance : 기존에 db에 저장되어 있던 값들 가져옴
        # request.user : 로그인한 user
        form = CustomUserChangeForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect("articles:index")
    else: # POST 요청이 아닐 때
        form = CustomUserChangeForm(instance = request.user)
    
    # get요청 or 유효성 검사 실패 했을 때
    context = {
        'form':form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method== "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 세션 무효화 방지(자동 로그아웃 방지)
            # hash 함수로 현재 사용자의 인증 세션 갱신
            update_session_auth_hash(request, user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form':form,
    }
    return render(request, "accounts/change_password.html", context)