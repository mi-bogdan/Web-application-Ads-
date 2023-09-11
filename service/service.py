from ads.models import Ip, Advertisement

from django_filters import rest_framework as filters


def get_client_ip(request) -> str:
    """Метод для получения АЙПИ"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        # В REMOTE_ADDR значение айпи пользователя
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_ip_advertisement(ip, advertisement) -> None:
    """Добавление IP к посту для подсчета просмотров"""

    if Ip.objects.filter(ip=ip).exists():
        advertisement.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        advertisement.views.add(Ip.objects.get(ip=ip))


class FiltersPriceAds(filters.FilterSet):
    """Фильтрация объявления по цене"""
    price = filters.RangeFilter(field_name='price')

    class Meta:
        model = Advertisement
        fields = ['price']
