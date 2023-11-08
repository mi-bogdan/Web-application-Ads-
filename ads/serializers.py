from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Advertisement, Comments, Like, ViolationReport, Favourites, Category

from djoser.serializers import UserCreateSerializer


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


class AdvertisementCreateSerializers(serializers.ModelSerializer):
    """Объявление"""
    class Meta:
        model = Advertisement
        fields = '__all__'


class CommentsCreateSerializers(serializers.ModelSerializer):
    """Добавления комментария к объявлению"""

    class Meta:
        model = Comments
        fields = '__all__'


class CommentsSerializers(serializers.ModelSerializer):
    """Добавления комментария к объявлению"""
    children = RecursiveSerializer(many=True)
    user = serializers.SlugRelatedField(
            slug_field='first_name', read_only=True)

    class Meta:
        list_serializer_class = FilterCommentsListSerializer
        model = Comments
        fields = ('user', 'text', 'create_at', 'children')


class AdvertisementDeteilSerializers(serializers.ModelSerializer):
    """Полное объявление"""
    category = serializers.SlugRelatedField(slug_field='title', read_only=True)
    city = serializers.SlugRelatedField(slug_field='title', read_only=True)
    user = serializers.SlugRelatedField(
        slug_field='first_name', read_only=True)
    comments = CommentsSerializers(many=True)
    count_views = serializers.IntegerField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        exclude = ('views', 'slug', 'update_at',)

    def get_like_count(self, obj):
        return obj.like_set.count()


class LikeSerializers(serializers.ModelSerializer):
    """Добавления лайка к объявлению"""
    class Meta:
        model = Like
        fields = '__all__'


class ViolationReportSerializers(serializers.ModelSerializer):
    """Отправка сообщения о нарушении"""

    class Meta:
        model = ViolationReport
        fields = '__all__'


class CustomUserCreateSerializer(UserCreateSerializer):
    """Изменения полей для регистрации"""
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'email', 'password')


class FavouritesSerializer(serializers.ModelSerializer):
    """Добавления в избранное объявление"""
    class Meta:
        model = Favourites
        fields = '__all__'


class GetFavoritesAdsSerializer(serializers.ModelSerializer):
    """Вывод изранных объявлений"""
    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'img', 'price')


class GetFavouritesSerializer(serializers.ModelSerializer):
    """Вывод избранных объявлений для пользователя"""
    advertisement = GetFavoritesAdsSerializer()

    class Meta:
        model = Favourites
        fields = ('id', 'advertisement',)


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(read_only=True)

    def get_subcategories(self, category):
        subcategories = Category.objects.filter(parent=category)
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ['id', 'title', 'subcategories']
