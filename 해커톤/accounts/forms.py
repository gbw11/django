from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from medicines.models import Medicine


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, label='이메일 (선택)')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    current_medicines = forms.ModelMultipleChoiceField(
        queryset=Medicine.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='현재 복용 중인 약품'
    )

    class Meta:
        model = UserProfile
        fields = (
            'age', 'gender', 'height', 'weight',
            'conditions', 'is_pregnant', 'is_breastfeeding',
            'current_medicines'
        )
        widgets = {
            'conditions': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'age': '나이',
            'gender': '성별',
            'height': '키 (cm)',
            'weight': '몸무게 (kg)',
            'conditions': '지병 / 만성질환',
            'is_pregnant': '임신 중',
            'is_breastfeeding': '수유 중',
        }