from django.db import models
from django.contrib.auth.models import User
from mptt.models import TreeForeignKey, MPTTModel


class Ip(models.Model):
    """Таблица айпи адресов"""
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Category(MPTTModel):
    """Категории"""
    title = models.CharField(verbose_name='Названия', max_length=100)
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    parent = TreeForeignKey(
        'self', verbose_name="Родитель", related_name='children', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "Category"


class City(models.Model):
    title = models.CharField(verbose_name='Город', max_length=150)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        db_table = "City"


class Advertisement(models.Model):
    """Объявления"""
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    descriptions = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        verbose_name='Цена', max_digits=10, decimal_places=2)
    create_at = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True)
    update_at = models.DateTimeField(
        verbose_name="Дата обновления", auto_now=True)
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    views = models.ManyToManyField(Ip, related_name="post_views", blank=True)
    publication_params = models.JSONField(
        verbose_name='Детали', blank=True, null=True)
    telephone = models.CharField(verbose_name='Телефон', max_length=12)
    city = models.ForeignKey(City, verbose_name='Город',
                             on_delete=models.PROTECT)
    img = models.ImageField(verbose_name="Изображение",
                            upload_to='photo/%Y/%m/%d', null=True)
    slug = models.SlugField(verbose_name='Слаг', unique=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Объвление"
        verbose_name_plural = "Объявления"
        db_table = "Advertisement"


class Comments(models.Model):
    """Комментарии"""

    user = models.CharField(verbose_name="Имя", max_length=100)
    text = models.TextField(verbose_name="Текст", max_length=5000)
    perents = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True,related_name='children')
    advertisement = models.ForeignKey(
        Advertisement, verbose_name="Объявление", on_delete=models.CASCADE, related_name='comments')
    create_at = models.DateTimeField(
        verbose_name="Дата комментария", auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.user}"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        db_table = "Comments"


class Favourites(models.Model):
    """Избранное"""
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(
        Advertisement, verbose_name="Объявление", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}-{self.advertisement}"

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        db_table = "Favourites"


class ViolationReport(models.Model):
    """Отчет о нарушении"""
    TYPE = (
        ('сек', 'материалы сексуального характера'),
        ('оск', 'опасный или оскорбительный контент'),
        ('аза', 'контент, связанный с азартными онлайн-играми'),
    )
    REPORT_STATUS = (
        ('отк', 'открыт'),
        ('рас', 'рассмотрен'),
        ('зак', 'закрыт'),
    )
    the_complainer_user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True)
    advertisement = models.ForeignKey(
        Advertisement, verbose_name="Объявление", on_delete=models.CASCADE)
    types_of_violations = models.CharField(
        verbose_name='Тип нарушения', choices=TYPE, max_length=3)
    description_of_the_violation = models.TextField(
        verbose_name='Описание нарушения')
    report_status = models.CharField(
        verbose_name='Статус нарушения', choices=REPORT_STATUS, max_length=3)

    def __str__(self) -> str:
        return f'{self.advertisement}-{self.the_complainer_user}'

    class Meta:
        verbose_name = "Отчет о нарушении"
        verbose_name_plural = "Отчет о нарушениях"
        db_table = "ViolationReport"


class ImageAdvertisement(models.Model):
    """Изображение к продуктам"""

    img = models.ImageField(verbose_name="Изображение объявления",
                            upload_to='advertisement_images/%Y/%m/%d')
    advertisement = models.ForeignKey(
        Advertisement, verbose_name="Объявление", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.advertisement}'

    class Meta:
        verbose_name = "Изображение к объявлению"
        verbose_name_plural = "Изображения к объявлениям"
        db_table = "ImageAdvertisement"


class Like(models.Model):
    """Лайки"""
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    ads = models.ForeignKey(
        Advertisement, verbose_name='Объявление', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user}-{self.ads}'

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        db_table = "Like"


class Messages(models.Model):
    """Сообщения"""
    text = models.TextField(verbose_name='Текст сообщения')
    sender = models.ForeignKey(
        User, verbose_name='Отправитель', on_delete=models.SET_NULL, null=True, related_name='user_sender')
    recipient = models.ForeignKey(
        User, verbose_name='Получатель', on_delete=models.SET_NULL, null=True, related_name='user_recipient')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.text}-{self.recipient}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        db_table = "Messages"
