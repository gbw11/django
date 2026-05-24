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
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '약품'


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



class MedicineIngredient(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, verbose_name='함량')

    class Meta:
        verbose_name = '약품 성분'

class PersonalizedDosage(models.Model):
    """연령/상태별 맞춤 복용 정보"""
    AGE_GROUP_CHOICES = [
        ('infant',  '영아 (0~23개월)'),
        ('child',   '소아 (2~11세)'),
        ('teen',    '청소년 (12~17세)'),
        ('adult',   '성인 (18~64세)'),
        ('elderly', '고령자 (65세 이상)'),
    ]

    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE,
        related_name='personalized_dosages', verbose_name='약품'
    )
    age_group = models.CharField(
        max_length=10, choices=AGE_GROUP_CHOICES, verbose_name='연령 그룹'
    )
    dosage_info = models.TextField(verbose_name='복용량/방법')
    special_precautions = models.TextField(blank=True, verbose_name='해당 그룹 특이 주의사항')
    is_contraindicated = models.BooleanField(
        default=False, verbose_name='해당 그룹 금기 여부'
    )

    def __str__(self):
        return f"{self.medicine.name} - {self.get_age_group_display()}"

    class Meta:
        verbose_name = '맞춤 복용 정보'
        unique_together = ('medicine', 'age_group')