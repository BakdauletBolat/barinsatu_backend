from django.forms import fields
from .models import Ad, AdImage, AdType, AreaDetail, HomeDetail, RentType, RepairType, BuildingType, AdDetailType, City
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from authentication.serializers import UserSerializer


class HomeDetailSerializer(serializers.ModelSerializer):

    class Meta:

        model = HomeDetail
        fields = ('__all__')


class AreaDetailSerializer(serializers.ModelSerializer):

    class Meta:

        model = AreaDetail
        fields = ('__all__')


class AdObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, HomeDetail):
            return HomeDetailSerializer(value).data
        elif isinstance(value, AreaDetail):
            return AreaDetailSerializer(value).data

        raise Exception('Unexpected type of tagged object')


class AdDetailTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','name',)
        model = AdDetailType


class AdTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','name',)
        model = AdType


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','name',)
        model = City

class AdImageSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('id','image')
        model = AdImage

class AdSerializer(serializers.ModelSerializer):

    details = AdObjectRelatedField(read_only=True)

    images = AdImageSerializer(read_only=True,many=True)

    # Детальная информация
    ad_detail_type = AdDetailTypeSerializer(required=False)
    ad_detail_type_id = serializers.IntegerField()

    # Продажа или аренда
    ad_type_id = serializers.IntegerField()
    ad_type = AdTypeSerializer(required=False)

    # Город
    city_id = serializers.IntegerField()
    city = CitySerializer(required=False)

    # Автор
    author_id = serializers.IntegerField()
    author = UserSerializer(required=False)

    # Дом детальная
    numbers_room = serializers.IntegerField(required=False)
    total_area = serializers.IntegerField(required=False)
    floor = serializers.IntegerField(required=False)
    year_construction = serializers.IntegerField(required=False)
    repair_type_id = serializers.IntegerField(required=False)
    building_type_id = serializers.IntegerField(required=False)

    # Участок
    area = serializers.IntegerField(required=False)

    def create(self, validated_data):
        print(validated_data)
        detail = AdDetailType.objects.get(
            id=validated_data.get('ad_detail_type_id'))

        if detail.name == 'homedetail':

            try:
                numbers_room = validated_data.pop('numbers_room')
            except KeyError:
                numbers_room = None

            try:
                total_area = validated_data.pop('total_area')
            except KeyError:
                total_area = None

            try:
                floor = validated_data.pop('floor')
            except KeyError:
                floor = None

            try:
                year_construction = validated_data.pop('year_construction')
            except KeyError:
                year_construction = None

            try:
                repair_type_id = validated_data.pop('repair_type_id')
            except KeyError:
                repair_type_id = None

            try:
                building_type_id = validated_data.pop('building_type_id')
            except KeyError:
                building_type_id = None

            detail = HomeDetail.objects.create(
                numbers_room=numbers_room,
                total_area=total_area,
                floor=floor,
                year_construction=year_construction,
                repair_type_id=repair_type_id,
                building_type_id=building_type_id,
            )
        elif detail.name == 'areadetail':
            try:
                area = validated_data.pop('area')
            except KeyError:
                area = None

            detail = AreaDetail.objects.create(
                area=area
            )
        else:
            detail = None

        instance = Ad.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            ad_detail_type_id=validated_data['ad_detail_type_id'],
            ad_type_id=validated_data['ad_type_id'],
            city_id=validated_data['city_id'],
            author_id=validated_data['author_id'],
            price=validated_data['price'],
            details=detail
        )

        return instance

    class Meta:
        fields = ('__all__')
        model = Ad


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:

        fields = ('__all__')
        model = ContentType
