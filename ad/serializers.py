from django.forms import fields
from .models import (Ad, AdComments, AdImage, AdLike, AdType, AreaDetail,
             Communications, HomeDetail, RentType, RepairType, BuildingType,
             AdDetailType, City,ApartmentDetail)
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from authentication.serializers import UserSerializer


class BuildingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildingType
        fields = ('__all__')

class CommunicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Communications
        fields = ('__all__')

class RepairTypeSerializer(serializers.ModelSerializer):
    class Meta:

        model = RepairType
        fields = ('__all__')

class RentTypeSerializer(serializers.ModelSerializer):
    class Meta:

        model = RentType
        fields = ('__all__')    

class HomeDetailSerializer(serializers.ModelSerializer):


    building_type = BuildingTypeSerializer()
    repair_type = RepairTypeSerializer()

    total_area_string = serializers.SerializerMethodField()

    def get_total_area_string(self,obj):

        return f"{obj.total_area} м²"

    class Meta:

        model = HomeDetail
        fields = ('__all__')


class AreaDetailSerializer(serializers.ModelSerializer):

    communications = CommunicationSerializer(many=True)

    total_area_string = serializers.SerializerMethodField()

    def get_total_area_string(self,obj):

        if obj.unit_of_measure == 0:
            return f"{obj.total_area} сот"
        
        if obj.unit_of_measure == 1:
            return f"{obj.total_area} Га"

        return f"{obj.total_area}"

    class Meta:

        model = AreaDetail
        fields = ('__all__')


class ApartmentSerializer(serializers.ModelSerializer):

    building_type = BuildingTypeSerializer()
    repair_type = RepairTypeSerializer()

    total_area_string = serializers.SerializerMethodField()

    def get_total_area_string(self,obj):

        return f"{obj.total_area} м²"

    class Meta:
        model = ApartmentDetail
        fields = ('__all__')


class AdObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, HomeDetail):
            return HomeDetailSerializer(value).data
        elif isinstance(value, AreaDetail):
            return AreaDetailSerializer(value).data

        elif isinstance(value, ApartmentDetail):
            return ApartmentSerializer(value).data

        raise Exception('Unexpected type of tagged object')


class AdDetailTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','name','title')
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


class IsLikedSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(isLiked=True)
        return super(IsLikedSerializer, self).to_representation(data)

class AdLikeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = AdLike
        list_serializer_class = IsLikedSerializer 

class AdCommentSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        fields = ('__all__')
        read_only_fields = ('author',)
        model = AdComments

class MarkerAdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id','lat','lng')
        model = Ad
    

class AdSerializer(serializers.ModelSerializer):

    details = AdObjectRelatedField(read_only=True)
    images = AdImageSerializer(read_only=True,many=True)
    # Детальная информация
    ad_detail_type_id = serializers.IntegerField(write_only=True)
    ad_detail_type = AdDetailTypeSerializer(read_only=True)
    # Продажа или аренда
    ad_type_id = serializers.IntegerField(write_only=True)
    ad_type = AdTypeSerializer(read_only=True)
    # Город
    city_id = serializers.IntegerField(write_only=True)
    city = CitySerializer(read_only=True)

    # Автор
    author = UserSerializer(read_only=True)

    likes = AdLikeSerializer(many=True,read_only=True)
    comments = AdCommentSerializer(many=True,read_only=True)

    UNIT = (
        (0, 'Сот'),
        (1, 'Га')
    )
    

    # Дом детальная
    numbers_room = serializers.IntegerField(required=False)
    total_area = serializers.FloatField(required=False)
    floor = serializers.IntegerField(required=False)
    total_floor = serializers.IntegerField(required=False)
    year_construction = serializers.IntegerField(required=False)
    repair_type_id = serializers.IntegerField(required=False)
    building_type_id = serializers.IntegerField(required=False)
    communications = serializers.ListField(required=False)
    is_pledge = serializers.BooleanField(required=False)
    is_divisibility = serializers.BooleanField(required=False)
    unit_of_measure = serializers.IntegerField(default=0,required=False)

    comment_count = serializers.SerializerMethodField(read_only=True)



    def get_comment_count(self, obj):
        count = len(obj.comments.all())
        return count


    def create(self, validated_data):
        detail = AdDetailType.objects.get(
            id=validated_data.get('ad_detail_type_id'))

        if detail.title == 'homedetail':

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
        elif detail.title == 'apartmentdetail':

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
                repair_type_id = 1

            try:
                building_type_id = validated_data.pop('building_type_id')
            except KeyError:
                building_type_id = 1

            try:
                total_floor = validated_data.pop('total_floor')
            except KeyError:
                total_floor = None

            detail = ApartmentDetail.objects.create(
                numbers_room=numbers_room,
                total_area=total_area,
                floor=floor,
                total_floor=total_floor,
                
                year_construction=year_construction,
                repair_type_id=repair_type_id,
                building_type_id=building_type_id,
            )
        elif detail.title == 'areadetail':
            try:
                total_area = validated_data.pop('total_area')
            except KeyError:
                total_area = None

            try:
                is_pledge = validated_data.pop('is_pledge')
            except KeyError:
                is_pledge = 0

            try:
                is_divisibility = validated_data.pop('is_divisibility')
            except KeyError:
                is_divisibility = 0
            
            try:
                unit_of_measure = validated_data.pop('unit_of_measure')
            except KeyError:
                unit_of_measure = 0

            
            
            detail = AreaDetail.objects.create(
                total_area=total_area,
                is_pledge=is_pledge,
                unit_of_measure=unit_of_measure,
                is_divisibility=is_divisibility,
            )

            try:
                communications = validated_data.pop('communications')
                print(communications)
                for c in communications:  
                    cObject = Communications.objects.get(id=c) 
                    detail.communications.add(cObject)
            except KeyError:
                communications = None

        else:
            detail = None

        instance = Ad(
            title=validated_data['title'],
            location_text=validated_data['location_text'] or 'Место положение не указано',
            lat=validated_data['lat'] or 0,
            lng=validated_data['lng'] or 0,
            description=validated_data['description'],
            ad_detail_type_id=validated_data['ad_detail_type_id'],
            ad_type_id=validated_data['ad_type_id'],
            city_id=validated_data['city_id'],
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




