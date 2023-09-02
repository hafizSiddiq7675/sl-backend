from django.contrib import admin
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase


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


class RecipeRequirementAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'ingredient', 'quantity']
    list_filter = ['menu_item', 'ingredient']
    search_fields = ['menu_item__item_name', 'ingredient__name']
    ordering = ['menu_item']


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'purchase_date', 'customer_name', 'quantity', 'total_price']
    list_filter = ['menu_item', 'purchase_date']
    search_fields = ['menu_item__item_name', 'customer_name']
    ordering = ['-purchase_date', 'menu_item']
    readonly_fields = ['total_price']


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(RecipeRequirement, RecipeRequirementAdmin)
admin.site.register(Purchase, PurchaseAdmin)
