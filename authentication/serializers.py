from dataclasses import field
from rest_framework import serializers
from .models import NotifcationType, Notification, Rating, User, UserType
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserType
        fields = '__all__'


class UserLoginSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = UserSerializer(self.user).data
        return data

    

class UserSerializer(serializers.ModelSerializer):

    user_type = UserTypeSerializer(required=False,read_only=True)
    user_type_id = serializers.IntegerField(required=False,write_only=True)

    ratings_count = serializers.SerializerMethodField()

    def get_ratings_count(self,obj):
        return obj.ratings.all().length

    avatar = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id','name','surname','email','user_type','avatar','about','password','user_type_id','phone','ratings_count']
        extra_kwargs = {'password': {'write_only': True}}

    
class RatingSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Rating
        fields =("__all__")
    
class NotifcationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifcationType
        fields =("__all__")
    
class NotificicationSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    user__id = serializers.IntegerField(write_only=True)
    author = UserSerializer(read_only=True)
    type = NotifcationTypeSerializer(read_only=True)
    type_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Notification
        fields =("__all__")