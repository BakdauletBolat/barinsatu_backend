from django.http import JsonResponse
from .models import Ad, AdDetailType, AdImage, AdType,City
from rest_framework.generics import ListCreateAPIView,ListAPIView
from .serializers import AdSerializer, AdTypeSerializer, CitySerializer, ContentTypeSerializer,AdDetailTypeSerializer
from django.contrib.contenttypes.models import ContentType
from rest_framework import status


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

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return JsonResponse({"ads": serializer.data})

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