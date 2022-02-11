from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .permisions import AuthorPermission
from authentication.models import User, UserType
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.serializers import UserLoginSerializer, UserSerializer, UserTypeSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


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
    filterset_fields = ['user_type_id']
    ordering_fields = ['id']




class UserMe(APIView,LoginRequiredMixin):

    def get(self,request):
        if request.user.is_authenticated:
            user = UserSerializer(request.user,context={"request":request})
            return JsonResponse({"user":user.data})
        return JsonResponse({"detail":"user is not authenticated"},status=status.HTTP_401_UNAUTHORIZED)