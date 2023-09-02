from django.urls import path
from .views import UserLoginView

urlpatterns = [
    path('api/login/', UserLoginView.as_view(), name='user-login'),
]
