from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm

# Create your views here.
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


# def logout(request):
#     auth_logout(request)
#     return redirect('articles:index')


# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('articles:index')
#     else:
#         # UserCustom을 했기 때문에(AUTH_USER_MODEL 수정) 
#         # Meta 클래스의 User model을 변경해야 함
#         # form = UserCreationForm() 
#         form = CustomUserCreationForm()

#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)


# def delete(request):
#     request.user.delete()
#     return redirect('articles:index')