from django.urls import path, include

from .views import AdvertisementListApi, AdvertisementDeteilApi, CommentsCreateApi, LikeAPIView, ViolationReportView


urlpatterns = [
    path('ads/', AdvertisementListApi.as_view()),
    path('ads/<pk>/', AdvertisementDeteilApi.as_view()),
    path('comments/', CommentsCreateApi.as_view()),
    path('like/<pk>/', LikeAPIView.as_view()),
    path('report/', ViolationReportView.as_view()),
]
