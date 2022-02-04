from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from authentication.serializers import UserSerializer
from .models import Ad, AdComments, AdDetailType, AdImage, AdLike, AdType, BuildingType,City, RepairType
from rest_framework.generics import ListCreateAPIView,ListAPIView
from .serializers import (AdCommentSerializer, AdLikeSerializer, AdSerializer, AdTypeSerializer, 
                         BuildingTypeSerializer, CitySerializer, ContentTypeSerializer,
                         AdDetailTypeSerializer, RepairTypeSerializer)
from django.contrib.contenttypes.models import ContentType
from rest_framework.filters import OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import IntegrityError

class BuildingTypeListView(ListAPIView):
    serializer_class = BuildingTypeSerializer
    queryset = BuildingType.objects.all()

class RepairTypeListView(ListAPIView):
    serializer_class = RepairTypeSerializer
    queryset = RepairType.objects.all()

class CityListView(ListAPIView):

    serializer_class = CitySerializer
    queryset = City.objects.all()

class AdTypeListView(ListAPIView):
    
    serializer_class = AdTypeSerializer
    queryset = AdType.objects.all()

class AdDetailTypeListView(ListAPIView):
    
    serializer_class = AdDetailTypeSerializer
    queryset = AdDetailType.objects.all()







class AdListCreateView(ListCreateAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    filter_backends = [OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['ad_type','homedetail__building_type']
    ordering_fields = ['id']
    pagination_class = LimitOffsetPagination
    

    # def list(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_queryset().filter(home__id=1), many=True)
    #     return JsonResponse({"ads": serializer.data})

    def perform_create(self, serializer):
        instance = serializer.save()
        images = self.request.FILES.getlist('images')

        for image in images:
            AdImage.objects.create(
                image=image,
                ad=instance
            )
        return instance

class ContentTypeListCreateView(ListCreateAPIView):
    
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()


class CommentListCreateView(ListCreateAPIView):

    serializer_class = AdCommentSerializer
    queryset = AdComments.objects.all()

    def list(self, request, *args, **kwargs):
        ad_id = kwargs['pk']
        serializer = self.get_serializer(self.get_queryset().filter(ad_id=ad_id), many=True)
        return JsonResponse(serializer.data,safe=False)

    def perform_create(self, serializer):
        instance = serializer.save(
            author = self.request.user
        )
        return instance

@api_view()
def likeAd(request,pk):
    try:
        like = AdLike()
        like.ad = get_object_or_404(Ad, pk=pk)
        like.user = request.user
        like.save()
        print(like.isLiked)
        likeS = AdLikeSerializer(like).data
        return Response(likeS)

    except IntegrityError as e:
        ad = Ad.objects.get(id=pk)
        like = AdLike.objects.get(user=request.user,ad=ad)
        if like.isLiked:
            like.isLiked = False
        else:
            like.isLiked = True
        like.save()
        print(like.isLiked)
        likeS = AdLikeSerializer(like).data
        return Response(likeS)
        

    
