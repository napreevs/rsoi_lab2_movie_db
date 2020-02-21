import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import User
from .serializers import UserSerializer, UserPasswordSerializer


# Create your tests here.
class UserViewTest(APITestCase):
    client = APIClient()
    url = reverse('get_post_user')

    def setUp(self):
        User.objects.create(username='username1', email='email1@gmail.com', password='password')
        User.objects.create(username='username2', email='email2@gmail.com', password='password')
        User.objects.create(username='username3', email='email3@gmail.com', password='password')

    def test_get_all_users(self):
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        res = {'users': serialized.data}

        response = self.client.get(self.url)
        self.assertEqual(res, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_add_new_user(self):
        user = {
            'username': 'username4',
            'email': 'email4@gmail.com',
            'password': 'password'
        }

        response = self.client.post(
            self.url, data=json.dumps(user), content_type='application/json'
        )
        # self.assertEqual(user, response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_add_user_with_exist_username(self):
        user = {
            'username': 'username1',
            'email': 'email10@gmail.com',
            'password': 'password'
        }

        response = self.client.post(
            self.url, data=json.dumps(user), content_type='application/json'
        )
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)

    def test_add_user_with_exist_email(self):
        user = {
            'username': 'username10',
            'email': 'email1@gmail.com',
            'password': 'password'
        }

        response = self.client.post(
            self.url, data=json.dumps(user), content_type='application/json'
        )
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)


class UserInfoView(APITestCase):
    client = APIClient()

    def setUp(self):
        User.objects.create(username='username1', email='email1@gmail.com', password='password')
        User.objects.create(username='username2', email='email2@gmail.com', password='password')
        User.objects.create(username='username3', email='email3@gmail.com', password='password')

    def test_get_user_by_id(self):
        user = User.objects.get(username='username1')
        serialized = UserSerializer(user)
        id = serialized.data['id']
        response = self.client.get(
            reverse('get_put_delete_user', args=(id,))
        )
        self.assertEqual(serialized.data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
