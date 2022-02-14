from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from rest_framework.generics import ListCreateAPIView
from .models import Story, StoryComments, StoryLike
from .serializers import StoryCommentSerializer, StoryLikeSerializer, StorySerilizer
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.

class StoryListView(ListCreateAPIView):
    
    serializer_class = StorySerilizer
    queryset = Story.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['id']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'data':serializer.data})


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