from django.urls import path
from .views import (AdListCreateView,ContentTypeListCreateView,AdTypeListView,
                   AdDetailTypeListView,CityListView,CommentListCreateView,
                   BuildingTypeListView,RepairTypeListView,
                   likeAd)
urlpatterns = [
    path('',AdListCreateView.as_view()),
    path('create/',AdListCreateView.as_view()),
    path('type/',AdTypeListView.as_view()),
    path('type-detail/',AdDetailTypeListView.as_view()),
    path('comments/<int:pk>/',CommentListCreateView.as_view()),
    path('comments/',CommentListCreateView.as_view()),
    # path('rent-time/',RentTimeListView.as_view()),
    path('city/',CityListView.as_view()),
    path('content-types/',ContentTypeListCreateView.as_view()),
    path('building-types/',BuildingTypeListView.as_view()),
    path('repair-types/',RepairTypeListView.as_view()),
    path('like/<int:pk>/',likeAd)
]
