from django.urls import path
from .views import (AdCreateView, AdListView, CommunicationsListView,ContentTypeListCreateView,AdTypeListView,
                   AdDetailTypeListView,CityListView,CommentListView,CommentCreateView,
                   BuildingTypeListView,RepairTypeListView,AdRetrieveUpdateDestroyAPIView,
                   LikeAd,AdListMapView,ViewAd)
urlpatterns = [
    path('',AdListView.as_view()),
    path('map/',AdListMapView.as_view()),
    path('view/<int:pk>/',ViewAd.as_view),
    path('create/',AdCreateView.as_view()),
    path('edit-delete/<int:pk>/',AdRetrieveUpdateDestroyAPIView.as_view()),
    path('type/',AdTypeListView.as_view()),
    path('type-detail/',AdDetailTypeListView.as_view()),
    path('comments/<int:pk>/',CommentListView.as_view()),
    path('comments/',CommentCreateView.as_view()),
    path('city/',CityListView.as_view()),
    path('content-types/',ContentTypeListCreateView.as_view()),
    path('building-types/',BuildingTypeListView.as_view()),
    path('communications/',CommunicationsListView.as_view()),
    path('repair-types/',RepairTypeListView.as_view()),
    path('like/<int:pk>/',LikeAd.as_view())
]
