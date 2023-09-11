from django.urls import path, include

from .views import AdvertisementListApi, AdvertisementDeteilApi, CommentsCreateApi, LikeAPIView, ViolationReportView, AddFavouritesView, FavouritesView, remove_favorites, CreateAdvertisementApi, CategoryView, SortedCategoryAdsView


urlpatterns = [
    path('ads/', AdvertisementListApi.as_view()),
    path('create-ads/', CreateAdvertisementApi.as_view()),
    path('ads/<pk>/', AdvertisementDeteilApi.as_view()),
    path('comments/', CommentsCreateApi.as_view()),
    path('like/<pk>/', LikeAPIView.as_view()),
    path('report/', ViolationReportView.as_view()),
    path('add-favorite-ads/', AddFavouritesView.as_view()),
    path('favorite-ads/', FavouritesView.as_view()),
    path('delete-favorite/<pk>/', remove_favorites, name='remove-favorite'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('ads-categories/<pk>/', SortedCategoryAdsView.as_view()),
]
