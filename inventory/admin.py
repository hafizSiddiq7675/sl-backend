from django.contrib import admin
from .models import Ingredient


class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'available_quantity',
        'measurement_unit',
        'price_per_unit',
        'date_added',
        'expiry_date',
    ]
    list_filter = ['measurement_unit', 'date_added', 'expiry_date']
    search_fields = ['name']
    ordering = ['name']



admin.site.register(Ingredient, IngredientAdmin)
