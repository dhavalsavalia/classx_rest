import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from classifieds.api.serializers import (AreaSerializer, GroupSerializer,
                                         ImageSerializer, ItemSerializer)
from classifieds.models import Area, Group, Image, Item, Section, Profile


class RegistrationTestCase(APITestCase):
    def setUp(self):
        data = {
            'username': 'testcase',
            'email': 'test@test.com',
            'password1': 'Jht3rfT$',
            'password2': 'Jht3rfT$',
        }
        self.response = self.client.post(
            "/rest-auth/registration/",
            data
        )
        self.token = self.response.json()['key']

    def test_registration(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class ItemTestCase(APITestCase):

    list_url = reverse("item-list")

    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase",
            password="Jht3rfT$"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_item_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_create_authenticated(self):
        section = Section.objects.create(title='Section 1')
        group = Group.objects.create(title='Group 1', section=section)
        area = Area.objects.create(title='Area 1', slug='area-1')
        data = {
            'user': self.user.id,
            'title': 'Test Item',
            'description': 'Test Description',
            'price': 1500.00,
            'is_active': True,
            'area': {"id": area.id},
            'group': {"id": group.id}
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.get().title, data['title'])
