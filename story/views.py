from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListCreateAPIView
from .models import Story, StoryComments, StoryLike
from .serializers import StoryCommentSerializer, StoryLikeSerializer, StorySerilizer
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class StoryListView(ListCreateAPIView):
    
    serializer_class = StorySerilizer
    
    queryset = Story.objects.filter(is_archive=False)
    filterset_fields = ['author']
    filter_backends = [OrderingFilter,DjangoFilterBackend]
    ordering_fields = ['id']


class StoryArchiveView(APIView):

    def get(self,request,pk):

        ad = get_object_or_404(Story,id=pk)
        ad.is_archive = True
        ad.save()

        return JsonResponse({'status': 'archived story '+pk})



class StoryCreateView(CreateAPIView):

    serializer_class = StorySerilizer
    queryset = Story.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save(
            author = self.request.user
        )
        return instance

class CommentCreateView(CreateAPIView):

    serializer_class = StoryCommentSerializer
    queryset = StoryComments.objects.all()
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        instance = serializer.save(
            author = self.request.user
        )
        return instance


class ViewStory(APIView):
    def get(self,request,pk):
        try:
            story = get_object_or_404(Story, id=pk)
            story.views += 1
            story.save()
            return JsonResponse({'status':'ok'})
        except IntegrityError as e:
            print(e)
            return JsonResponse({'status':'failed'})

class LikeStory(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self,request,pk):
        try:
            like = StoryLike()
            like.story = get_object_or_404(Story, pk=pk)
            like.user = request.user
            like.save()
            print(like.isLiked)
            likeS = StoryLikeSerializer(like).data
            return Response(likeS)

        except IntegrityError as e:
            story = Story.objects.get(id=pk)
            like = StoryLike.objects.get(user=request.user,story=story)
            if like.isLiked:
                like.isLiked = False
            else:
                like.isLiked = True
            like.save()
            print(like.isLiked)
            likeS = StoryLikeSerializer(like).data
            return Response(likeS)