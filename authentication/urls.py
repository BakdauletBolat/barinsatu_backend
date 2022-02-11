from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (UserCreateListView, UserMe,UserLoginView,UserRetriveView,
                    UserTypeListView,UserRetrieveUpdateDestroyAPIView,UserListView)
from django.urls import path

urlpatterns = [
    path('token/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserCreateListView.as_view()),
    path('update-delete/<int:pk>/',UserRetrieveUpdateDestroyAPIView.as_view()),
    path('profile/<int:pk>/',UserRetriveView.as_view()),
    path('users/',UserListView.as_view()),
    path('user-types/',UserTypeListView.as_view()),
    path('me/',UserMe.as_view())
]