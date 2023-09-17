from django.urls import path, include

from .views import AdvertisementListApi, AdvertisementDeteilApi, CommentsCreateApi, LikeAPIView, ViolationReportView, AddFavouritesView, FavouritesView, remove_favorites, CreateAdvertisementApi, CategoryView, SortedCategoryAdsView


urlpatterns = [
    path('ads/', AdvertisementListApi.as_view(), name='ads'),
    path('create-ads/', CreateAdvertisementApi.as_view(), name='create-ads'),
    path('ads/<pk>/', AdvertisementDeteilApi.as_view(), name='deteil-ads'),
    path('comments/', CommentsCreateApi.as_view(), name='comments-create'),
    path('like/<pk>/', LikeAPIView.as_view(), name='like'),
    path('report/', ViolationReportView.as_view(), name='report'),
    path('add-favorite-ads/', AddFavouritesView.as_view(), name='add-favorite-ads'),
    path('favorite-ads/', FavouritesView.as_view(), name='favorite-ads'),
    path('delete-favorite/<pk>/', remove_favorites, name='remove-favorite'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('ads-categories/<pk>/',
         SortedCategoryAdsView.as_view(), name='ads-categories'),
]
