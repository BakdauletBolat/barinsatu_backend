from django.urls import path
from .views import StoryListView,StoryCreateView,CommentCreateView,LikeStory

urlpatterns = [
    
    path('',StoryListView.as_view()),
    path('create/',StoryCreateView.as_view()),
    path('comment-create/',CommentCreateView.as_view()),
    path('like-story/<int:pk>/',LikeStory.as_view())
]