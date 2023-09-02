from django.contrib import admin
from .models import Ingredient, MenuItem


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


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'price']
    search_fields = ['item_name']
    ordering = ['item_name']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
