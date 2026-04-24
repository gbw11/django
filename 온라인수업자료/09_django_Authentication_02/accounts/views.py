from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    # 로그인한 사용자는 로그인 할 필요가 없음
    if request.user.is_authenticated:
        return redirect('articles:index')

    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
        pass
    else:
        form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('articles:index')

def signup(request):
    # 로그인한 사용자는 회원가입할 필요가 없음
    if request.user.is_authenticated:
        return redirect('articles:index')
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 회원 가입 후 로그인
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()

    context ={
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    # 아래 두 줄의 순서 중요 !delete => 세션 삭제하기!
    request.user.delete()
    auth_logout(request) # 세션 삭제
    return redirect("articles:index")