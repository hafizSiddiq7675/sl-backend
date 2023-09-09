from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Ingredient
from unittest import mock


class GetIngredientApiViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            'ingredient-list'
        )  # replace with the name of your URL pattern for GetIngredientApiView

        # create a sample user
        self.user = User.objects.create_user(
            username='sampleuser', password='samplepassword'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_unauthenticated_request(self):
        # Remove authentication credentials and make the request
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)  # 401 is Unauthorized

    def test_get_ingredients(self):
        # Create some sample ingredients
        Ingredient.objects.create(
            name='Salt', available_quantity=10, price_per_unit=0.5
        )
        Ingredient.objects.create(
            name='Sugar', available_quantity=5, price_per_unit=0.75
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_no_ingredients(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'No ingredients found')


class DeleteIngredientApiViewTests(APITestCase):
    def setUp(self):
        # Creating a test user and setting up the client to use this user.
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Creating a sample ingredient.
        self.ingredient = ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            available_quantity=100.5,  # FloatField value, represents the available quantity
            measurement_unit=Ingredient.GRAMS,  # Choosing Grams as the measurement unit from the given choices
            price_per_unit=5.50,  # DecimalField value for price per unit
            expiry_date='2025-01-01',  # Optional: a sample expiry date
        )

    def test_successful_deletion(self):
        url = reverse(
            'ingredient-delete', kwargs={'ingredient_id': self.ingredient.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Ingredient.objects.filter(id=self.ingredient.id).exists()
        )

    def test_ingredient_not_found(self):
        non_existent_id = self.ingredient.id + 1
        url = reverse(
            'ingredient-delete', kwargs={'ingredient_id': non_existent_id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)

    def test_unauthorized_access(self):
        # Unauthenticating the client.
        self.client.force_authenticate(user=None)
        url = reverse(
            'ingredient-delete', kwargs={'ingredient_id': self.ingredient.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)

    def test_server_error(self):
        url = reverse(
            'ingredient-delete', kwargs={'ingredient_id': self.ingredient.id}
        )

        with mock.patch(
            'inventory.views.DeleteIngredientApiView.delete',
            side_effect=Exception,
        ):
            with self.assertRaises(
                Exception
            ):  # Expecting the Exception to be raised here
                self.client.delete(url)
