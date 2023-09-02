from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, pagination
from .models import Ingredient
from .serializers import IngredientSerializer


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
