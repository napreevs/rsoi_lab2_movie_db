import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import (
    Movie,
    MovieFeature,
    MovieInfo,
    Feature,
)
from .serializers import (
    MovieInfoSerializer,
    MovieSerializer
)


# Create your tests here.
class MovieViewTest(APITestCase):
    client = APIClient()
    url = reverse('get_post_movies')
    url2 = reverse('post_features')

    def setUp(self):
        movie1 = Movie.objects.create(
            title='Movie1', release_year=2010,
            director='director', writer='writer', genre='genre',
            description='a', country='USA', rating=8, box_office=100000000
        )

        movie2 = Movie.objects.create(
            title='Movie2', release_year=2010,
            director='director', writer='writer', genre='genre',
            description='a', country='USA', rating=8, box_office=100000000
        )

        feature1 = Feature.objects.create(title='feature1')
        feature2 = Feature.objects.create(title='feature2')

        MovieFeature.objects.create(movie=movie1, feature=feature1, description="description")
        MovieFeature.objects.create(movie=movie2, feature=feature2, description="description")
        MovieFeature.objects.create(movie=movie2, feature=feature1, description="description")

    def test_get_all_movies(self):
        movies = MovieInfo.objects.all()
        serialized = MovieInfoSerializer(movies, many=True)
        response = self.client.get(self.url)

        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_add_new_movie(self):
        movie = {
            'title': 'Movie3',
            'release_year': 2010,
            'director': 'a',
            'writer': 'a',
            'genre': 'a',
            'description': 'a',
            'country': 'USA',
            'rating': 8,
            'box_office': 10000000
        }

        response = self.client.post(
            self.url, data=json.dumps(movie), content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_add_new_feature(self):
        feature = {
            'title': "new_feature"
        }
        response = self.client.post(
            self.url2, data=json.dumps(feature), content_type='application/json'
        )
        self.assertEqual(feature['title'], response.data['title'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_movie_add_feature(self):
        feature = Feature.objects.create(title='some_feature')
        movie_id = Movie.objects.filter(title='Movie1')[0].id
        movie_feature = {
            'feature_id': feature.id,
            'description': 'description'
        }

        response = self.client.post(
            reverse('post_moviefeatures', kwargs={'movie_id': movie_id}),
            data=json.dumps(movie_feature),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_nonexist_movie_add_feature(self):
        feature = Feature.objects.create(title='some_feature')
        movie_id = 100000
        movie_feature = {
            'feature_id': feature.id,
            'description': 'description'
        }

        response = self.client.post(
            reverse('post_moviefeatures', kwargs={'movie_id': movie_id}),
            data=json.dumps(movie_feature),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)