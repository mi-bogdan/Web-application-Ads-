from django.urls import path, include

from .views import AdvertisementListApi, AdvertisementDeteilApi, CommentsCreateApi


urlpatterns = [
    path('ads/', AdvertisementListApi.as_view()),
    path('ads/<pk>/', AdvertisementDeteilApi.as_view()),
    path('add/', CommentsCreateApi.as_view()),
]
