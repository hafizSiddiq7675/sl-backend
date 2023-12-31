from rest_framework import serializers
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = [
            'id',
            'name',
            'available_quantity',
            'price_per_unit',
            'date_added',
            'expiry_date',
            'measurement_unit',
        ]


class MenuItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='item_name')

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']

    def validate_name(self, value):
        if self.instance and self.instance.item_name == value:
            # This is for update scenarios. If the name hasn't changed during update, then it's okay.
            return value

        if MenuItem.objects.filter(item_name=value).exists():
            raise serializers.ValidationError(
                'A menu item with this name already exists.'
            )
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                'Price must be greater than or equal to zero.'
            )
        return value


class RecipeRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeRequirement
        fields = ['menu_item', 'ingredient', 'quantity']

    def validate(self, data):
        # You can add any additional validation here
        return data


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = [
            'menu_item',
            'purchase_date',
            'customer_name',
            'quantity',
            'total_price',
        ]
