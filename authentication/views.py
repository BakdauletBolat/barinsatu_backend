
import json
from django.shortcuts import get_object_or_404
from rest_framework.validators import ValidationError
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView,CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .permisions import AuthorPermission
from authentication.models import Notification, Rating, User, UserType
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.serializers import NotificicationSerializer, RatingSerializer, UserLoginSerializer, UserSerializer, UserTypeSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from ad.serializers import AdSerializer
from ad.models import Ad

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    user = UserSerializer(user).data
    return {
        "user":user,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserLoginView(TokenObtainPairView):

    serializer_class = UserLoginSerializer

class UserCreateListView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            return serializer.save(
                avatar=self.request.data.get('avatar')
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = get_tokens_for_user(user)

        return JsonResponse(data, status=status.HTTP_201_CREATED, headers=headers)


class UserFavoriteView(ListAPIView):

    serializer_class = AdSerializer

    def get_queryset(self):
        id = self.kwargs['pk']
        user = get_object_or_404(User,id=id)
        print(user)
        ad_favorites = []
        for favorite in user.likes.all():
            print(favorite)
            ad_favorites.append(favorite.ad)
        return ad_favorites


class UserRateList(ListAPIView):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.kwargs['pk'])

class UserRateCreate(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        return instance

class NotificationListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        notifcationList = Notification.objects.filter(user=request.user)
        print(notifcationList)
        return JsonResponse(NotificicationSerializer(notifcationList,many=True).data,safe=False)

    def post(self,request,pk):
        data = request.POST
        print(data)
        text = ''
        if data.get('text') != None:
            text = data['text']
        else:
            text = ''
        users = User.objects.filter(user_type_id=pk)
        for user in users:
            Notification.objects.create(
                text=text,
                user=user,
                author=request.user,
                type_id=pk
            )
            print('saved')
        
        return JsonResponse({"response":True})


class NotifcationReadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        notifcationList = Notification.objects.filter(user=request.user)
        for notifcation in notifcationList:
            notifcation.is_readed = True
            notifcation.save()
            
        return JsonResponse({"readed":True})

class NotificationCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        notifcationList = Notification.objects.filter(user=request.user)
        return JsonResponse(NotificicationSerializer(notifcationList,many=True).data,safe=False)

    def post(self,request):
        data = json.loads(request.body)
        text = ''
        print(data)


        try:
             text = data['text']
        except KeyError:
            text = ''

        if data['type_id'] == None and data['user_id'] == None:
            raise ValidationError('Поля обязательны')

        Notification.objects.create(
            text=text,
            user_id=data['user_id'],
            author=request.user,
            type_id=data['type_id']
        )

        
        return JsonResponse({"response":True})

class UserRetriveView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserTypeListView(ListAPIView):
    serializer_class = UserTypeSerializer
    queryset = UserType.objects.all()


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    permission_classes = [AuthorPermission]
    queryset = User.objects.all()

class UserListView(ListAPIView):

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [OrderingFilter,DjangoFilterBackend]
    filterset_fields = ['user_type']
    ordering_fields = ['id']




class UserMe(APIView,LoginRequiredMixin):

    def get(self,request):
        if request.user.is_authenticated:
            user = UserSerializer(request.user,context={"request":request})
            return JsonResponse({"user":user.data})
        return JsonResponse({"detail":"user is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)