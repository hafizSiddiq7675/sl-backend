from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, pagination
from .models import Ingredient, MenuItem
from .serializers import (
    IngredientSerializer,
    MenuItemSerializer,
    RecipeRequirementSerializer,
    PurchaseSerializer,
)


class GetIngredientApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IngredientSerializer
    pagination_class = pagination.PageNumberPagination

    def get(self, request):
        try:
            ingredients = Ingredient.objects.all()

            if not ingredients.exists():
                return Response(
                    {'error': 'No ingredients found'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Implementing pagination
            paginator = self.pagination_class()
            paginated_ingredients = paginator.paginate_queryset(
                ingredients, request
            )

            if paginated_ingredients is not None:
                serializer = self.serializer_class(
                    paginated_ingredients, many=True
                )
                return paginator.get_paginated_response(serializer.data)

            # This part will handle if there's no pagination required
            serializer = self.serializer_class(ingredients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DeleteIngredientApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, ingredient_id):
        try:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            ingredient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Ingredient.DoesNotExist:
            return Response(
                {'error': 'Ingredient not found'},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {'error': 'Internal Server Error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetMenuItemApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MenuItemSerializer
    pagination_class = pagination.PageNumberPagination

    def get(self, request):
        try:
            menu_items = MenuItem.objects.all()

            if not menu_items.exists():
                return Response(
                    {'error': 'No menu items found'},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Implementing pagination
            paginator = self.pagination_class()
            paginated_menu_items = paginator.paginate_queryset(
                menu_items, request
            )

            if paginated_menu_items is not None:
                serializer = self.serializer_class(
                    paginated_menu_items, many=True
                )
                return paginator.get_paginated_response(serializer.data)

            # This part will handle if there's no pagination required
            serializer = self.serializer_class(menu_items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': 'Internal Server Error', 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class StoreMenuItemApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MenuItemSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class StoreIngredientApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IngredientSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class StoreRecipeRequirementApiView(APIView):
    # Only authenticated users can access this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecipeRequirementSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class StorePurchaseApiView(APIView):
    # Only authenticated users can access this view
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PurchaseSerializer

    def post(self, request):
        # Validate menu_item ID
        menu_item_id = request.data.get('menu_item')
        if not MenuItem.objects.filter(id=menu_item_id).exists():
            return Response(
                {'detail': 'MenuItem not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()  # The total_price is calculated in the save method of the Purchase model
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class UpdateIngredientApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = IngredientSerializer

    def patch(self, request, ingredient_id):
        try:
            ingredient = Ingredient.objects.get(pk=ingredient_id)
        except Ingredient.DoesNotExist:
            return Response(
                {'detail': 'Ingredient not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Partial update (only fields provided in the request payload)
        serializer = self.serializer_class(
            instance=ingredient, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
