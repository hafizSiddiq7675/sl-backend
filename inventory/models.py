from django.db import models
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    # Choices for the measurement_unit field
    GRAMS = 'grams'
    LITERS = 'liters'
    PIECES = 'pieces'
    MEASUREMENT_CHOICES = [
        (GRAMS, 'Grams'),
        (LITERS, 'Liters'),
        (PIECES, 'Pieces'),
    ]

    # Fields
    name = models.CharField(
        max_length=255, unique=True, verbose_name='Ingredient Name'
    )
    available_quantity = models.FloatField(
        validators=[MinValueValidator(0)], verbose_name='Available Quantity'
    )
    measurement_unit = models.CharField(
        max_length=10,
        choices=MEASUREMENT_CHOICES,
        verbose_name='Measurement Unit',
    )
    price_per_unit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='Price per Unit',
    )
    date_added = models.DateField(
        auto_now_add=True, null=True, blank=True, verbose_name='Date Added'
    )
    expiry_date = models.DateField(
        null=True, blank=True, verbose_name='Expiry Date'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    # Fields
    item_name = models.CharField(max_length=255, verbose_name='Menu Item Name')
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Price',
    )

    class Meta:
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'

    def __str__(self):
        return self.item_name


class RecipeRequirement(models.Model):
    # Fields
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, verbose_name="Menu Item")
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, verbose_name="Ingredient")
    quantity = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Quantity")

    class Meta:
        verbose_name = "Recipe Requirement"
        verbose_name_plural = "Recipe Requirements"
        unique_together = ['menu_item', 'ingredient']
        # Creating indexes on fields for optimizing query performance
        indexes = [
            models.Index(fields=['menu_item',]),
            models.Index(fields=['ingredient',]),
        ]

    def __str__(self):
        return f"{self.menu_item} - {self.ingredient}"