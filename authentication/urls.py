from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (NotificationCreateView, NotificationListCreateView, UserCreateListView, UserMe,UserLoginView,UserRetriveView,
                    UserTypeListView,UserRetrieveUpdateDestroyAPIView,UserListView,
                    UserRateCreate,UserRateList)
from django.urls import path

urlpatterns = [
    path('token/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',UserCreateListView.as_view()),
    path('update-delete/<int:pk>/',UserRetrieveUpdateDestroyAPIView.as_view()),
    path('profile/<int:pk>/',UserRetriveView.as_view()),
    path('users/',UserListView.as_view()),
    path('user-types/',UserTypeListView.as_view()),
    path('me/',UserMe.as_view()),
    path('rate/',UserRateCreate.as_view()),
    path('rate-list/<int:pk>/',UserRateList.as_view()),
    path('notifications/',NotificationListCreateView.as_view()),
    path('notification-auto-create/<int:pk>',NotificationListCreateView.as_view()),
    path('notification-create/',NotificationCreateView.as_view())
]