from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Ingredient, MenuItem
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


class GetMenuItemApiViewTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser1', password='testpass'
        )
        cls.url = reverse('menu-items-list')

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_successful_response(self):
        # Create a sample menu item
        MenuItem.objects.create(item_name='Test Item', price=10.00)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Item', str(response.data))

    def test_no_menu_items(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
        self.assertIn('No menu items found', str(response.data))

    def test_internal_server_error(self):
        # Mocking an error scenario
        url = reverse('menu-items-list')

        with mock.patch(
            'inventory.views.GetMenuItemApiView.get',
            side_effect=Exception,
        ):
            with self.assertRaises(
                Exception
            ):  # Expecting the Exception to be raised here
                self.client.get(url)

    def test_unauthorized_access(self):
        # Create a new client without authentication
        client = APIClient()
        response = client.get(self.url)
        self.assertEqual(response.status_code, 401)

    def test_pagination(self):
        # Create more than the page limit, say if the limit is 10
        for _ in range(15):
            MenuItem.objects.create(item_name=f'Test Item {_}', price=10.00)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('count', response.data)
        self.assertEqual(response.data['count'], 15)


class StoreMenuItemApiViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(
            'store-menu-item'
        )  # Assuming the name you provided in urls.py is 'store-menu-item'
        self.client = APIClient()

        # Assuming you have a User model to use for authentication.
        self.user = User.objects.create_user(
            username='testuser2', password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_menu_item(self):
        data = {'name': 'Chicken Alfredo', 'price': '10.99'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['price'], data['price'])

    def test_duplicate_item_name(self):
        MenuItem.objects.create(item_name='Chicken Alfredo', price=10.99)
        data = {'name': 'Chicken Alfredo', 'price': '12.99'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'name', response.data
        )  # Expecting an error related to the 'name' field

    def test_price_validation(self):
        data = {'name': 'Chicken Alfredo', 'price': '-5.00'}  # Invalid price
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'price', response.data
        )  # Expecting an error related to the 'price' field

    def test_unauthenticated_access(self):
        self.client.logout()  # Removing authentication
        data = {'name': 'Chicken Alfredo', 'price': '10.99'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 401)


class StoreIngredientApiViewTests(APITestCase):
    def setUp(self):
        # Sample User for testing
        self.user = User.objects.create_user(
            username='testuser3', password='testpassword'
        )

        # Setup the APIClient with credentials for authentication
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # URL for the API endpoint
        self.url = reverse('store-ingredient')

        # Sample valid data
        self.valid_data = {
            'name': 'Tomato',
            'available_quantity': 150.0,
            'measurement_unit': 'grams',
            'price_per_unit': 0.50,
        }

    def test_create_ingredient_successful(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertEqual(Ingredient.objects.get().name, 'Tomato')

    def test_unauthenticated_create_ingredient(self):
        # Force unauthentication
        self.client.force_authenticate(user=None)

        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_ingredient_name_uniqueness(self):
        # Create one ingredient with the name "Tomato"
        Ingredient.objects.create(
            name='Tomato',
            available_quantity=100,
            measurement_unit='grams',
            price_per_unit=0.30,
        )

        # Try to create another ingredient with the same name
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_measurement_unit(self):
        # Change the valid measurement unit to an invalid one
        self.valid_data['measurement_unit'] = 'invalid_unit'

        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_available_quantity(self):
        # Set available_quantity to a negative value
        self.valid_data['available_quantity'] = -10

        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_price_per_unit(self):
        # Set price_per_unit to a negative value
        self.valid_data['price_per_unit'] = -0.30

        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, 400)
