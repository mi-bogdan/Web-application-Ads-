from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.core.files import File
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Advertisement, Category, City, Comments, Like, ViolationReport, Favourites
from .serializers import FavouritesSerializer,GetFavouritesSerializer

from PIL import Image
import io
import mock
import json


class AdsTest(APITestCase):
    def setUp(self) -> None:
        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'photo.jpg'

        self.user_test_1 = User.objects.create_user(
            username='test1', password='1qy67ui78')
        self.user_test_1.save()
        self.user_test_2 = User.objects.create_user(
            username='test2', password='1qjlm32&n8')
        self.user_test_2.save()

        self.category_1 = Category.objects.create(
            title='Недвижимость',
            slug='nedvijimost'
        )

        self.category_2 = Category.objects.create(
            title='Квартиры',
            slug='kvartiru',
            parent=self.category_1
        )

        self.city_1 = City.objects.create(title='Макеевка')

        self.ads_one = Advertisement.objects.create(
            title='Продам квартиру',
            descriptions='Тут описание объявления',
            price=3000000,
            category=self.category_2,
            user=self.user_test_1,
            publication_params={"Квадрат": 23, "Площадь": 56},
            telephone='+79490000000',
            city=self.city_1,
            img=self.file_mock.name,
            slug='prodaja_kavartiru'
        )

        self.data_comments_one = {
            "user": self.user_test_1.id,
            "text": "Очень интересно",
            "advertisement": self.ads_one.id
        }

        self.user1_test_token = Token.objects.create(user=self.user_test_1)

        self.favourite1 = Favourites.objects.create(
            user=self.user_test_1, advertisement=self.ads_one)

    def test_create_invalid_ads(self):
        data_ads = {
            "title": "Продам квартиру 2",
            "descriptions": "Тут описание объявления",
            "price": 1000000,
            "category": self.category_2.id,
            "user": self.user_test_1.id,
            "publication_params": {"авто": 23, "Кузов": 56},
            "telephone": "+79490000000",
            "city": self.city_1.id,
            "img": self.file_mock.name,
            "slug": "prodaja_avto_2"

        }

        response = self.client.post(
            reverse('create-ads'), data_ads, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_ads(self):
        response = self.client.get(reverse('ads'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        ads = response.data[0]

        self.assertEqual(ads['title'], self.ads_one.title)

    def test_deteil_valide_ads(self):
        response = self.client.get(
            reverse('deteil-ads', kwargs={'pk': self.ads_one.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), self.ads_one.title)

    def test_deteil_invalide_ads(self):
        response = self.client.get(reverse('deteil-ads', kwargs={'pk': 10000}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comments_unauthenticated(self):
        response = self.client.post(
            reverse('comments-create'), self.data_comments_one, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_comments(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user1_test_token.key)
        response = self.client.post(
            reverse('comments-create'), self.data_comments_one, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comments.objects.count(), 1)
        self.assertEqual(Comments.objects.first().advertisement, self.ads_one)

    def test_create_comment_invalid_post(self):
        data = {
            "user": self.user_test_1.id,
            "text": "Очень интересно",
            "advertisement": 999
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user1_test_token.key)
        response = self.client.post(
            reverse('comments-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comments.objects.count(), 0)

    def test_like_ads(self):
        like = {
            "user": self.user_test_1.id,
            "ads": self.ads_one.id
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user1_test_token.key)
        response = self.client.put(
            reverse('like', kwargs={'pk': self.ads_one.id}), like, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(
            user=self.user_test_1, ads=self.ads_one).exists())

    def test_like_delete_ads(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword')

        like = Like.objects.create(user=user, ads=self.ads_one)
        self.client.force_authenticate(user=user)
        url = reverse('like', kwargs={'pk': self.ads_one.id})
        response = self.client.put(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(
            user=user, ads=self.ads_one).exists())

    def test_report_valid_ads(self):
        data = {
            "advertisement": self.ads_one.id,
            "types_of_violations": "оск",
            "description_of_the_violation": "ужасно не возможно смотреть"
        }
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user1_test_token.key)
        response = self.client.post(
            reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ViolationReport.objects.count(), 1)

    def test_report_unauthenticated(self):
        data = {
            "advertisement": self.ads_one.id,
            "types_of_violations": "оск",
            "description_of_the_violation": "ужасно не возможно смотреть"
        }

        response = self.client.post(
            reverse('report'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_list(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_category_list_ads(self):
        response = self.client.get(
            reverse('ads-categories', kwargs={'pk': self.category_2.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ads = response.data[0]
        self.assertEqual(len(response.data), 1)
        self.assertEqual(ads['title'], self.ads_one.title)

    def test_add_favorite_ads(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user1_test_token.key)
        data = {'ads_id': self.ads_one.id}
        response = self.client.post(reverse('add-favorite-ads'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content),
                         FavouritesSerializer(Favourites.objects.get()).data)

    def test_favorite_unauthenticated_ads(self):
        data = {'ads_id': self.ads_one.id}
        response = self.client.post(reverse('add-favorite-ads'), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_favourite_nonexistent_ads(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.user1_test_token.key)
        data = {'ads_id': 999999}
        response = self.client.post(reverse('add-favorite-ads'), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content), {
                         'error': 'Advertisement not found.'})
        


