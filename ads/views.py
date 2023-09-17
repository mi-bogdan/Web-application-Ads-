from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view

from service.service import get_client_ip, add_ip_advertisement, FiltersPriceAds
from django.db.models import Count

from .models import Advertisement, Like, Favourites, Category
from .serializers import AdvertisementListSerializers, AdvertisementDeteilSerializers, CommentsCreateSerializers, LikeSerializers, ViolationReportSerializers, FavouritesSerializer, GetFavouritesSerializer, AdvertisementCreateSerializers, CategorySerializer

from django_filters.rest_framework import DjangoFilterBackend


class AdvertisementListApi(APIView):
    """Вывод объявлений"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        advertisement = Advertisement.objects.all()
        serializers = AdvertisementListSerializers(advertisement, many=True)
        return Response(serializers.data)


class AdvertisementDeteilApi(APIView):
    """Вывод подробной информации о объявлении"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            advertisement = Advertisement.objects.annotate(
                count_views=Count('views')).get(pk=pk)
            ip = get_client_ip(request)
            add_ip_advertisement(ip, advertisement)

            serealizers = AdvertisementDeteilSerializers(advertisement)
            return Response(serealizers.data, status=status.HTTP_200_OK)
        except Advertisement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateAdvertisementApi(generics.CreateAPIView):
    """Добавления объявления на сайт"""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AdvertisementCreateSerializers
    queryset = Advertisement.objects.all()


class CommentsCreateApi(APIView):
    """Добавления комментария к объявлению"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        comments = CommentsCreateSerializers(data=request.data)
        if comments.is_valid():
            comments.save(user=self.request.user)
            return Response(comments.data, status=201)
        return Response(status=400)


class LikeAPIView(APIView):
    """Обновления, удаления лайка"""

    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        user = request.user.id
        ads = Advertisement.objects.get(pk=pk)
        try:
            like = Like.objects.get(user=user, ads=ads)
            like.delete()  # удаление существующего лайка
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            serializer = LikeSerializers(
                data={'user': request.user.id, 'ads': pk})
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViolationReportView(APIView):
    """Отправление жалобы на объявление"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        report = ViolationReportSerializers(data=request.data)
        if report.is_valid():
            report.save(the_complainer_user=request.user)
        return Response(status=201)


class AddFavouritesView(APIView):
    """Добавление поста в избранное"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        ads_id = request.data.get('ads_id')
        try:
            ads = Advertisement.objects.get(id=ads_id)
        except Advertisement.DoesNotExist:
            return Response({'error': 'Advertisement not found.'}, status=status.HTTP_404_NOT_FOUND)
        favorite_post = Favourites.objects.create(user=user, advertisement=ads)
        serializer = FavouritesSerializer(favorite_post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FavouritesView(APIView):
    """Вывод избранных постов"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            favorites_post = Favourites.objects.filter(user=user)
            serializer = GetFavouritesSerializer(favorites_post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Favourites.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def remove_favorites(request, pk):
    """Удаление избраного объвления"""
    try:
        favorites = Favourites.objects.get(pk=pk)
        favorites.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Favourites.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer


class SortedCategoryAdsView(generics.ListAPIView):
    """Вывод объявлений по категориям и фильтрация по цене"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = AdvertisementListSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FiltersPriceAds

    def get_queryset(self):
        category_id = self.kwargs['pk']
        ads = Advertisement.objects.filter(category__id=category_id)
        filtered_ads = self.filter_queryset(ads)
        return filtered_ads
