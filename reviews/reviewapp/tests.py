import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Review
from .serializers import ReviewSerializer


# Create your tests here.
class ReviewViewTest(APITestCase):
    client = APIClient()
    url = reverse('reviews')

    def setUp(self):
        Review.objects.create(user_id=1, movie_id=1, rating=4.5, content='some review')
        Review.objects.create(user_id=1, movie_id=2, rating=4.5, content='some review')
        Review.objects.create(user_id=2, movie_id=2, rating=4.5, content='some review')

    def test_get_all_reviews(self):
        reviews = Review.objects.all()
        serialized = ReviewSerializer(reviews, many=True)
        response = self.client.get(self.url)
        self.assertEqual(response.data['reviews'], serialized.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_add_review(self):
        review = {
            'user_id': 3,
            'movie_id': 3,
            'rating': 4.3,
            'content': 'some review'
        }
        response = self.client.post(
            self.url, data=json.dumps(review), content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, review)

    def test_add_exist_review(self):
        review = {
            'user_id': 1,
            'movie_id': 1,
            'rating': 4.3,
            'content': 'some review'
        }
        response = self.client.post(
            self.url, data=json.dumps(review), content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_add_incorrect_review(self):
        review = {
            'movie_id': 1,
            'rating': 4.3,
            'content': 'some review'
        }
        response = self.client.post(
            self.url, data=json.dumps(review), content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_review(self):
        review = {
            'user_id': 1,
            'movie_id': 1,
            'rating': 4,
            'content': 'changed review'
        }
        response = self.client.put(
            self.url, data=json.dumps(review), content_type='application/json'
        )
        db_review = ReviewSerializer(Review.objects.get(user_id=1, movie_id=1))

        self.assertEqual(db_review.data, review)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_notexist_review(self):
        review = {
            'user_id': 10000,
            'movie_id': 10000,
            'rating': 4,
            'content': 'changed review'
        }
        response = self.client.put(
            self.url, data=json.dumps(review), content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_change_incorrect_review(self):
        review = {
            'movie_id': 10000,
            'rating': 4,
            'review': 'changed review'
        }
        response = self.client.put(
            self.url, data=json.dumps(review), content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewUserViewTest(APITestCase):
    client = APIClient()

    # url = reverse('user_reviews')

    def setUp(self):
        Review.objects.create(user_id=1, movie_id=1, rating=4.5, content='some review')
        Review.objects.create(user_id=1, movie_id=2, rating=4.5, content='some review')
        Review.objects.create(user_id=2, movie_id=2, rating=4.5, content='some review')

    def test_get_all_user_reviews(self):
        user_id = 1
        response = self.client.get(reverse('user_reviews', args=(user_id,)))
        user_reviews = ReviewSerializer(Review.objects.filter(user_id=user_id), many=True)
        self.assertEqual(response.data, user_reviews.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_all_user_reviews(self):
        user_id = 1
        response = self.client.delete(reverse('user_reviews', args=(user_id,)))
        user_reviews = Review.objects.filter(user_id=user_id)

        self.assertEqual(len(user_reviews), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ReviewMovieViewTest(APITestCase):
    client = APIClient()

    def setUp(self):
        Review.objects.create(user_id=1, movie_id=1, rating=4.5, content='some review')
        Review.objects.create(user_id=1, movie_id=2, rating=4.5, content='some review')
        Review.objects.create(user_id=2, movie_id=2, rating=4.5, content='some review')

    def test_get_all_movie_reviews(self):
        movie_id = 2
        response = self.client.get(reverse('movie_reviews', args=(movie_id,)))
        user_reviews = ReviewSerializer(Review.objects.filter(movie_id=movie_id), many=True)

        self.assertEqual(response.data['results'], user_reviews.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_all_movie_reviews(self):
        movie_id = 2
        response = self.client.delete(reverse('movie_reviews', args=(movie_id,)))
        user_reviews = Review.objects.filter(movie_id=movie_id)

        self.assertEqual(len(user_reviews), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)