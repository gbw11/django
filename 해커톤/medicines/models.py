from django.db import models

class Ingredient(models.Model):
    """성분 모델"""
    name = models.CharField(max_length=200, verbose_name='성분명')
    description = models.TextField(blank=True, verbose_name='설명')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '성분'


class Medicine(models.Model):
    """약품 모델"""
    CATEGORY_CHOICES = [
        ('OTC', '일반의약품'),
        ('ETC', '전문의약품'),
        ('SUPP', '건강기능식품'),
    ]

    name = models.CharField(max_length=200, verbose_name='제품명')
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name='분류')
    manufacturer = models.CharField(max_length=100, verbose_name='제조사')
    ingredients = models.ManyToManyField(Ingredient, through='MedicineIngredient', verbose_name='성분')
    usage = models.TextField(verbose_name='용도/효능')
    dosage = models.TextField(verbose_name='섭취/복용법')
    storage = models.TextField(verbose_name='보관법')
    precautions = models.TextField(verbose_name='주의사항')
    side_effects = models.TextField(verbose_name='부작용')
    contraindications = models.TextField(verbose_name='금기 조건')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '약품'


class MedicineIngredient(models.Model):
    """약품-성분 연결 (함량 포함)"""
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, verbose_name='함량')

    class Meta:
        verbose_name = '약품 성분'


class Interaction(models.Model):
    """약품 간 상호작용"""
    LEVEL_CHOICES = [
        ('CAUTION', '병용 주의'),
        ('FORBIDDEN', '병용 금기'),
    ]

    medicine_a = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='interactions_as_a')
    medicine_b = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='interactions_as_b')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, verbose_name='상호작용 수준')
    description = models.TextField(verbose_name='상호작용 설명')

    def __str__(self):
        return f"{self.medicine_a} ↔ {self.medicine_b} ({self.get_level_display()})"

    class Meta:
        verbose_name = '상호작용'


class UserProfile(models.Model):
    """사용자 상태 정보"""
    GENDER_CHOICES = [('M', '남성'), ('F', '여성'), ('O', '기타')]

    session_key = models.CharField(max_length=40, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True, verbose_name='나이')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    height = models.FloatField(null=True, blank=True, verbose_name='키(cm)')
    weight = models.FloatField(null=True, blank=True, verbose_name='몸무게(kg)')
    conditions = models.TextField(blank=True, verbose_name='지병')
    is_pregnant = models.BooleanField(default=False, verbose_name='임신 여부')
    is_breastfeeding = models.BooleanField(default=False, verbose_name='수유 여부')
    current_medicines = models.ManyToManyField(Medicine, blank=True, verbose_name='복용 중인 약')

    class Meta:
        verbose_name = '사용자 프로필'