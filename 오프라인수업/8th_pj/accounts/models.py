from django.db import models
# AbstractUser : User 관련된 기본적인 필드를 제공
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass