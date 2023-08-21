from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, permissions

from service.service import get_client_ip, add_ip_advertisement
from django.db.models import Count

from .models import Advertisement, Category, Like, ViolationReport
from .serializers import AdvertisementListSerializers, AdvertisementDeteilSerializers, CommentsCreateSerializers, LikeSerializers, ViolationReportSerializers


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
        advertisement = Advertisement.objects.annotate(
            count_views=Count('views')).get(pk=pk)
        ip = get_client_ip(request)
        add_ip_advertisement(ip, advertisement)

        serealizers = AdvertisementDeteilSerializers(advertisement)
        return Response(serealizers.data)


class CommentsCreateApi(APIView):
    """Добавления комментария к объявлению"""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        comments = CommentsCreateSerializers(data=request.data)
        if comments.is_valid():
            comments.save()
        return Response(status=201)


class LikeAPIView(APIView):
    """Обновления, удаления лайка"""

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        serializer = LikeSerializers(data={'user': request.user.id, 'ads': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
