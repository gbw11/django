from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# models.py의 User 모델을 가져옴
from .models import User

# Register your models here.
# admin 사이트에 등록하겠다(User모델, UserAdmin)
admin.site.register(User, UserAdmin)