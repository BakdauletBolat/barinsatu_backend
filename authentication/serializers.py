from dataclasses import field
from rest_framework import serializers
from .models import User, UserType


class UserTypeSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserType
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    user_type = UserTypeSerializer(required=False)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id','name','surname','email','user_type','avatar','about','password']
        extra_kwargs = {'password': {'write_only': True}}