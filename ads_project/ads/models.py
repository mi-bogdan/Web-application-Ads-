from django.db import models


class Category(models.Model):
    """Категории"""
    pass

class Advertisement(models.Model):
    """Объявления"""
    title=models.CharField(verbose_name='Заголовок',max_length=150)
    descriptions=models.TextField(verbose_name='Описание')
    create_at = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True)
    update_at = models.DateTimeField(
        verbose_name="Дата публикации", auto_now=True)

class Comments(models.Model):
    """Комментарии"""
    pass

class Favourites(models.Model):
    """Избранное"""
    pass

class ViolationReport(models.Model):
    """Отчет о нарушении"""
    pass