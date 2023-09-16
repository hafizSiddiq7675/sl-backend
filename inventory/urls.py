from django.urls import path
from .views import (
    GetIngredientApiView,
    DeleteIngredientApiView,
    GetMenuItemApiView,
    StoreMenuItemApiView,
    StoreIngredientApiView,
    StoreRecipeRequirementApiView,
    StorePurchaseApiView,
    UpdateIngredientApiView,
    GetMenuItemsApiView,
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
    path(
        'api/store-menu-item/',
        StoreMenuItemApiView.as_view(),
        name='store-menu-item',
    ),
    path(
        'api/store-ingredient/',
        StoreIngredientApiView.as_view(),
        name='store-ingredient',
    ),
    path(
        'api/store-reciperequirement/',
        StoreRecipeRequirementApiView.as_view(),
        name='store-reciperequirement',
    ),
    path(
        'api/store-purchase/',
        StorePurchaseApiView.as_view(),
        name='store-purchase',
    ),
    path(
        'api/update-ingredient/<int:ingredient_id>/',
        UpdateIngredientApiView.as_view(),
        name='update-ingredient',
    ),
    path(
        'api/get-menu-items/',
        GetMenuItemsApiView.as_view(),
        name='get-menu-items',
    ),
]
