from django.contrib import admin
from .models import Medicine, Ingredient, MedicineIngredient, Interaction, PersonalizedDosage

admin.site.register(Medicine)
admin.site.register(Ingredient)
admin.site.register(MedicineIngredient)
admin.site.register(Interaction)
admin.site.register(PersonalizedDosage)