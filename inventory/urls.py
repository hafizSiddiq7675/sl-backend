from django.urls import path
from .views import (
    GetIngredientApiView,
    DeleteIngredientApiView,
    GetMenuItemApiView,
)

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
    path(
        'api/menu-items/', GetMenuItemApiView.as_view(), name='menu-items-list'
    ),
]
