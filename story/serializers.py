from rest_framework.serializers import ModelSerializer,SerializerMethodField,ListSerializer

from authentication.models import User
from .models import Story, StoryComments, StoryLike
from authentication.serializers import UserSerializer

class IsLikedSerializer(ListSerializer):
    def to_representation(self, data):
        data = data.filter(isLiked=True)
        return super(IsLikedSerializer, self).to_representation(data)

class StoryLikeSerializer(ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = StoryLike
        list_serializer_class = IsLikedSerializer 


class StoryCommentSerializer(ModelSerializer):
   

    class Meta:
        fields = ('__all__')
        read_only_fields = ('author',)
        model = StoryComments

class StorySerilizer(ModelSerializer):

    story_likes = StoryLikeSerializer(many=True,read_only=True)
    story_comments = StoryCommentSerializer(many=True,read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:

        model = Story
        fields = ('__all__')

