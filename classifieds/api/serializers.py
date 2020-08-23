from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Item, Image, Area, Group


class AreaSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    title = serializers.StringRelatedField(read_only=True)
    slug = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Area
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    title = serializers.StringRelatedField(read_only=True)
    section = serializers.StringRelatedField(read_only=True)
    slug = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    slug = serializers.StringRelatedField(read_only=True)
    group = GroupSerializer()
    area = AreaSerializer()
    images = ImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        group_data = validated_data.pop('group')
        area_data = validated_data.pop('area')
        area_id = area_data['id']
        group_id = group_data['id']
        item = Item.objects.create(
            **validated_data,
            group=Group.objects.get(id=group_id),
            area=Area.objects.get(id=area_id),
            user=self.context['request'].user
        )
        return item
