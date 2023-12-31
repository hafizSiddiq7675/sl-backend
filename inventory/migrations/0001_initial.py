# Generated by Django 4.2.4 on 2023-09-02 06:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=255,
                        unique=True,
                        verbose_name='Ingredient Name',
                    ),
                ),
                (
                    'available_quantity',
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name='Available Quantity',
                    ),
                ),
                (
                    'measurement_unit',
                    models.CharField(
                        choices=[
                            ('grams', 'Grams'),
                            ('liters', 'Liters'),
                            ('pieces', 'Pieces'),
                        ],
                        max_length=10,
                        verbose_name='Measurement Unit',
                    ),
                ),
                (
                    'price_per_unit',
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        validators=[
                            django.core.validators.MinValueValidator(0.01)
                        ],
                        verbose_name='Price per Unit',
                    ),
                ),
                (
                    'date_added',
                    models.DateField(
                        auto_now_add=True, null=True, verbose_name='Date Added'
                    ),
                ),
                (
                    'expiry_date',
                    models.DateField(
                        blank=True, null=True, verbose_name='Expiry Date'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients',
            },
        ),
    ]
