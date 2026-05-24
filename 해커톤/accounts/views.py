from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm, ProfileForm
from .models import UserProfile


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'{user.username}님, 환영합니다! 먼저 내 정보를 입력해 주세요.')
            return redirect('/accounts/profile/edit/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.POST.get('next', '/'))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def profile_edit_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '내 정보가 저장되었습니다.')
            # next 파라미터가 있으면 해당 페이지로 복귀
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url if next_url else '/accounts/profile/')
    else:
        form = ProfileForm(instance=profile)
    next_url = request.GET.get('next', '')
    return render(request, 'accounts/profile_edit.html', {
        'form': form,
        'next': next_url
    })