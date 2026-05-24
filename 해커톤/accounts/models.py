from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = [('M', '남성'), ('F', '여성'), ('O', '기타')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='나이')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True, verbose_name='키(cm)')
    weight = models.FloatField(null=True, blank=True, verbose_name='몸무게(kg)')
    conditions = models.TextField(blank=True, verbose_name='지병')
    is_pregnant = models.BooleanField(default=False, verbose_name='임신 여부')
    is_breastfeeding = models.BooleanField(default=False, verbose_name='수유 여부')
    current_medicines = models.ManyToManyField(
        'medicines.Medicine', blank=True, verbose_name='복용 중인 약'
    )

    def get_age_group(self):
        """나이 그룹 반환"""
        if not self.age:
            return 'adult'
        if self.age < 2:
            return 'infant'       # 영아
        if self.age < 12:
            return 'child'        # 소아
        if self.age < 18:
            return 'teen'         # 청소년
        if self.age >= 65:
            return 'elderly'      # 고령자
        return 'adult'            # 성인

    def __str__(self):
        return f"{self.user.username}의 프로필"

    class Meta:
        verbose_name = '사용자 프로필'