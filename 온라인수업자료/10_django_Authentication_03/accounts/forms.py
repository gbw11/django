from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# get_user_model : 활성화된 user 모델 반환
from django.contrib.auth import get_user_model
# 위와 같은 방식을 사용하기 때문에 아래같이 import 하지않는다.
# ===> from . models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']