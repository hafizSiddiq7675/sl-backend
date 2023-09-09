from django.urls import path
from .views import GetIngredientApiView, DeleteIngredientApiView

urlpatterns = [
    path(
        'api/ingredients/',
        GetIngredientApiView.as_view(),
        name='ingredient-list',
    ),
    path(
        'api/ingredients/<int:ingredient_id>/',
        DeleteIngredientApiView.as_view(),
        name='ingredient-delete',
    ),
]
