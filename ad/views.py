from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.serializers import UserSerializer
from .models import Ad, AdComments, AdDetailType, AdImage, AdLike, AdType, BuildingType,City, Communications, RepairType
from rest_framework.generics import ListCreateAPIView,ListAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .serializers import (AdCommentSerializer, AdLikeSerializer, AdSerializer, AdTypeSerializer, 
                         BuildingTypeSerializer, CitySerializer, CommunicationSerializer, ContentTypeSerializer,
                         AdDetailTypeSerializer, RepairTypeSerializer)
from django.contrib.contenttypes.models import ContentType
from rest_framework.filters import OrderingFilter
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError
from .permisions import AuthorPermission


class CommunicationsListView(ListAPIView):
    serializer_class = CommunicationSerializer
    queryset = Communications.objects.all()

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

class AdFilter(FilterSet):
    class Meta:
        model = Ad
        fields = {
            'ad_type': ['exact'],
            'author': ['exact'],
            'ad_detail_type': ['exact'],
            'price': ['range'],
            'homedetail__numbers_room': ['range'],
            'homedetail__total_area': ['range'],
            'homedetail__floor': ['range'],
            'homedetail__building_type': ['exact'],
            'homedetail__repair_type': ['exact'],
            'apartmentdetail__numbers_room': ['range'],
            'apartmentdetail__total_area': ['range'],
            'apartmentdetail__floor': ['range'],
            'apartmentdetail__building_type': ['exact'],
            'apartmentdetail__repair_type': ['exact'],
            'areadetail__communications': ['exact'],
            'areadetail__is_pledge': ['exact'],
            'areadetail__is_divisibility': ['exact'],
            'areadetail__total_area': ['range']
        }

class AdListView(ListAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    filter_backends = [OrderingFilter,DjangoFilterBackend]
    filter_class = AdFilter
    ordering_fields = ['id']
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit =5


class AdListMapView(ListAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()




class AdCreateView(CreateAPIView):

    serializer_class = AdSerializer
    queryset = Ad.objects.all()
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.author = self.request.user
        instance.save()
        images = self.request.FILES.getlist('images')
        print(images)
        print(self.request.FILES)
        for image in images:
            AdImage.objects.create(
                image=image,
                ad=instance
            )
        return instance

class AdRetrieveUpdateDestroyAPIView(LoginRequiredMixin,RetrieveUpdateDestroyAPIView):
    serializer_class = AdSerializer
    queryset = Ad.objects.all()  
    permission_classes = [AuthorPermission,IsAuthenticated] 


class ContentTypeListCreateView(ListAPIView):
    
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()


class CommentListView(ListAPIView):

    serializer_class = AdCommentSerializer
    queryset = AdComments.objects.all()

    def list(self, request, *args, **kwargs):
        ad_id = kwargs['pk']
        serializer = self.get_serializer(self.get_queryset().filter(ad_id=ad_id), many=True)
        return JsonResponse(serializer.data,safe=False)

class CommentCreateView(CreateAPIView):

    serializer_class = AdCommentSerializer
    queryset = AdComments.objects.all()
    permission_classes = [IsAuthenticated] 

    def perform_create(self, serializer):
        instance = serializer.save(
            author = self.request.user
        )
        return instance

class LikeAd(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self,request,pk):
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
    
        

    
