from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from authentication.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.serializers import UserSerializer
from rest_framework import status

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    user = UserSerializer(user).data
    return {
        "user":user,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


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


class UserMe(APIView,LoginRequiredMixin):

    def get(self,request):
        if request.user.is_authenticated:
            user = UserSerializer(request.user)
            return JsonResponse({"user": user.data})
        return JsonResponse({"detail":"user is not authenticated"})