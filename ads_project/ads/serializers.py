from rest_framework import serializers
from .models import Advertisement, Category, Comments, Like


class FilterCommentsListSerializer(serializers.ListSerializer):
    """Фильтр комментариев только perents"""

    def to_representation(self, data):
        data = data.filter(perents=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(
            instance, context=self.context)
        return serializer.data


class AdvertisementListSerializers(serializers.ModelSerializer):
    """Список объявления"""
    city = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'city', 'img', 'create_at', 'price')


class CommentsCreateSerializers(serializers.ModelSerializer):
    """Добавления комментария к объявлению"""

    class Meta:
        model = Comments
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    """Добавления комментария к объявлению"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterCommentsListSerializer
        model = Comments
        fields = ('user', 'text', 'create_at', 'children')


class AdvertisementDeteilSerializers(serializers.ModelSerializer):
    """Полное объявление"""
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    city = serializers.SlugRelatedField(slug_field='title', read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    comments = CommentsSerializers(many=True)
    count_views = serializers.IntegerField()

    class Meta:
        model = Advertisement
        exclude = ('views', 'slug', 'update_at',)


class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
