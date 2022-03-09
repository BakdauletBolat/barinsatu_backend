from django.urls import path
from .views import StoryListView,StoryCreateView,CommentCreateView,LikeStory,ViewStory,StoryArchiveView

urlpatterns = [
    
    path('',StoryListView.as_view()),
    path('create/',StoryCreateView.as_view()),
    path('comment-create/',CommentCreateView.as_view()),
    path('view/<int:pk>/',ViewStory.as_view()),
    path('like-story/<int:pk>/',LikeStory.as_view()),
    path('archive/<int:pk>/',StoryArchiveView.as_view())
]