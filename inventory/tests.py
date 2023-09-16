from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
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


class StoreRecipeRequirementApiViewTest(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser4', password='testpass'
        )
        self.client = APIClient()

        # Create sample MenuItem and Ingredient for testing
        self.menu_item = MenuItem.objects.create(
            item_name='Test Item', price=10.00
        )
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            available_quantity=10.0,
            measurement_unit=Ingredient.GRAMS,
            price_per_unit=1.00,
        )

        # URL for the APIView
        self.url = reverse(
            'store-reciperequirement'
        )  # The exact name depends on your urls.py configuration

    def test_authenticated_with_valid_data(self):
        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # Valid data
        data = {
            'menu_item': self.menu_item.id,
            'ingredient': self.ingredient.id,
            'quantity': 5.0,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            RecipeRequirement.objects.filter(
                menu_item=self.menu_item, ingredient=self.ingredient
            ).exists()
        )

    def test_authenticated_with_invalid_data(self):
        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # Invalid data (quantity below 0)
        data = {
            'menu_item': self.menu_item.id,
            'ingredient': self.ingredient.id,
            'quantity': -5.0,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(
            RecipeRequirement.objects.filter(
                menu_item=self.menu_item, ingredient=self.ingredient
            ).exists()
        )

    def test_unauthenticated_request(self):
        # Do not authenticate the client

        # Some data
        data = {
            'menu_item': self.menu_item.id,
            'ingredient': self.ingredient.id,
            'quantity': 5.0,
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)


class StorePurchaseApiViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse(
            'store-purchase'
        )  # assuming 'store-purchase' is the name of your URL pattern for StorePurchaseApiView
        self.menu_item = MenuItem.objects.create(
            item_name='Sample Item', price=10.0
        )  # create a sample menu item

        # Create an authenticated user and obtain a token (assuming you're using token authentication)
        self.user = User.objects.create_user(
            username='testuser5', password='testpass'
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )  # set the token in the request headers

    def test_create_purchase(self):
        """Test creating a purchase."""
        data = {
            'menu_item': self.menu_item.id,
            'customer_name': 'John Doe',
            'quantity': 3,
            'total_price': 30,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Purchase.objects.count(), 1)
        self.assertEqual(
            Purchase.objects.get().total_price, 30.0
        )  # 10.0 * 3 = 30.0

    def test_invalid_menu_item(self):
        """Test validation for invalid menu item."""
        data = {
            'menu_item': 9999,  # non-existent menu item id
            'customer_name': 'John Doe',
            'quantity': 3,
            'total_price': 123,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 404)

    def test_invalid_quantity(self):
        """Test validation for invalid quantity."""
        data = {
            'menu_item': self.menu_item.id,
            'customer_name': 'John Doe',
            'quantity': -3,  # negative quantity
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)

    def test_unauthenticated_request(self):
        """Test request without authentication."""
        self.client.credentials()  # Remove credentials
        data = {
            'menu_item': self.menu_item.id,
            'customer_name': 'John Doe',
            'quantity': 3,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 401)


class UpdateIngredientApiViewTest(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser6', password='testpass'
        )

        # Create an ingredient
        self.ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            available_quantity=100.0,
            measurement_unit=Ingredient.GRAMS,
            price_per_unit=5.0,
        )
        self.url = reverse('update-ingredient', args=[self.ingredient.id])
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )  # set the token in the request headers

    def test_authenticated_user_can_update_ingredient(self):

        data = {'name': 'Updated Ingredient'}
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated Ingredient')

    def test_unauthenticated_user(self):
        self.client.credentials()  # Remove credentials
        data = {'name': 'Updated Ingredient'}
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, 401)

    def test_ingredient_does_not_exist(self):

        invalid_url = reverse(
            'update-ingredient', args=[999]
        )  # Assuming 999 does not exist
        data = {'name': 'Updated Ingredient'}
        response = self.client.patch(invalid_url, data)

        self.assertEqual(response.status_code, 404)

    def test_invalid_data(self):

        # Invalid measurement unit
        data = {'measurement_unit': 'invalid_unit'}
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, 400)

    def test_partial_update(self):

        original_price = '{:.2f}'.format(self.ingredient.price_per_unit)

        data = {'name': 'Partially Updated Ingredient'}
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Partially Updated Ingredient')
        self.assertEqual(
            response.data['price_per_unit'], str(original_price)
        )  # Ensure other fields remain unchanged


class GetMenuItemsApiViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Create some sample menu items
        MenuItem.objects.all().delete()
        MenuItem.objects.create(
            item_name='Grilled Chicken Sandwich', price=10.99
        )
        MenuItem.objects.create(item_name='Veggie Salad', price=7.49)
        MenuItem.objects.create(item_name='Chicken Salad', price=8.99)

    def test_get_menu_items(self):
        url = reverse('get-menu-items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)

    def test_search_menu_items(self):
        url = reverse('get-menu-items') + '?search=Chicken'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data['results']), 2
        )  # 2 items with "chicken" in their name

    def test_ordering_menu_items(self):
        url = reverse('get-menu-items') + '?ordering=price'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            float(response.data['results'][0]['price']), 7.49
        )  # The cheapest item

    def test_pagination(self):
        url = reverse('get-menu-items') + '?page=1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'results' in response.data
        )  # Check if paginated response structure is used
