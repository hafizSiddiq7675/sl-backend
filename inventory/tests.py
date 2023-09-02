from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Ingredient  # import your Ingredient model


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
