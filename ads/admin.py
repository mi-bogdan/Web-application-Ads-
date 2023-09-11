from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Advertisement, ImageAdvertisement, City, Like, Ip, Comments, Favourites, ViolationReport


class CategoryAdmin(MPTTModelAdmin):
    mptt_indent_field = 'title'
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title',)
    prepopulated_fields = {'slug': ('title',), }


admin.site.register(Category, CategoryAdmin)


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'create_at', 'update_at',
                    'category', 'user', 'telephone', 'city')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')




@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ads', 'created_at')
    list_display_links = ('id', 'user', 'ads')


@admin.register(Ip)
class IpAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip')
    list_display_links = ('id', 'ip')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'perents',
                    'advertisement', 'create_at')
    list_display_links = ('id', 'user')


@admin.register(ViolationReport)
class ViolationReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'the_complainer_user', 'advertisement',
                    'types_of_violations', 'description_of_the_violation', 'report_status','create_at')
    list_display_links = ('id', 'the_complainer_user', 'advertisement')


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'advertisement')
    list_display_links = ('id', 'user')


@admin.register(ImageAdvertisement)
class ImageAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'advertisement')
    list_display_links = ('id', 'advertisement')



