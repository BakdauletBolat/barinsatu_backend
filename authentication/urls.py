from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserCreateListView, UserMe,UserLoginView
from django.urls import path

urlpatterns = [
    path('token/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserCreateListView.as_view()),
    path('me/',UserMe.as_view())
]