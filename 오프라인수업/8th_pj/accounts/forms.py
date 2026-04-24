from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# get_user_model : AbstractUser 간접참조 함수

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model() # 간접 참조
        
        # 직접 참조 예시
        # model = User
        # fields = ()
