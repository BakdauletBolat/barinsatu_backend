from django.urls import path
from .views import AdListCreateView,ContentTypeListCreateView,AdTypeListView,AdDetailTypeListView,CityListView
urlpatterns = [
    path('',AdListCreateView.as_view()),
    path('create/',AdListCreateView.as_view()),
    path('type/',AdTypeListView.as_view()),
    path('type-detail/',AdDetailTypeListView.as_view()),
    path('city/',CityListView.as_view()),
    path('content-types/',ContentTypeListCreateView.as_view())
]
