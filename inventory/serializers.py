from rest_framework import serializers
from .models import Ingredient, MenuItem


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'available_quantity', 'price_per_unit']


class MenuItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='item_name')

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']
