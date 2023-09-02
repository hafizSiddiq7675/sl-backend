from django.urls import path
from .views import GetIngredientApiView

urlpatterns = [
    path(
        'api/ingredients/',
        GetIngredientApiView.as_view(),
        name='ingredient-list',
    ),
]
