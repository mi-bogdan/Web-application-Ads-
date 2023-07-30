from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from service.service import get_client_ip, add_ip_advertisement
from django.db.models import Count

from .models import Advertisement, Category,Like
from .serializers import AdvertisementListSerializers, AdvertisementDeteilSerializers, CommentsCreateSerializers,LikeSerializers


class AdvertisementListApi(APIView):
    """Вывод объявлений"""

    def get(self, request):
        advertisement = Advertisement.objects.all()
        serializers = AdvertisementListSerializers(advertisement, many=True)
        return Response(serializers.data)


class AdvertisementDeteilApi(APIView):
    """Вывод подробной информации о объявлении"""

    def get(self, request, pk):
        advertisement = Advertisement.objects.annotate(
            count_views=Count('views')).get(pk=pk)
        ip = get_client_ip(request)
        add_ip_advertisement(ip, advertisement)

        serealizers = AdvertisementDeteilSerializers(advertisement)
        return Response(serealizers.data)


class CommentsCreateApi(APIView):
    """Добавления комментария к объявлению"""

    def post(self, request):
        comments = CommentsCreateSerializers(data=request.data)
        if comments.is_valid():
            comments.save()
        return Response(status=201)
    

class LikeAPIView(APIView):
    
    def post(self, request, pk, format=None):
        serializer = LikeSerializers(data={'user': request.user.id, 'post': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk, format=None):
        user = request.user.id
        ads = Advertisement.objects.get(pk=pk)
        try:
            like = Like.objects.get(user=user, ads=ads)
            like.delete()  # remove existing like
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            like = Like(user=user, ads=ads)
            like.save()
            serializer = LikeSerializers(like)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
