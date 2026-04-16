from django.contrib import admin

# Register your models here.
# models.py로부터 Article 모델을 가져오겠다.
from .models import Article

# admin 사이트에 등록하겠다(Article을)
admin.site.register(Article)