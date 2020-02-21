from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status
import requests
from urllib.parse import urlparse

USER_HOST = 'http://localhost:8001/api'
MOVIE_HOST = 'http://localhost:8003/api'
REVIEW_HOST = 'http://localhost:8002/api'


def make_pagination_url(request, url):
    if url is None:
        return None
    request_url = request.path
    domain = request.META['HTTP_HOST']
    print(domain)
    result = 'http://' + domain + request_url + '?' + urlparse(url).query
    print(result)
    return result


# Create your views here.
class UserView(APIView):
    def get(self, request, pk):
        response = requests.get(url=USER_HOST + '/users/%d' % pk)
        return Response(data=response.json(), status=response.status_code)

    def put(self, request, pk):
        response = requests.put(url=USER_HOST + '/users/%d' % pk, data=request.data)
        return Response(data=response.json(), status=response.status_code)

    def delete(self, request, pk):
        response = requests.delete(url=USER_HOST + '/users/%d' % pk)
        if response.status_code != status.HTTP_200_OK:
            return Response(data=response.json(), status=response.status_code)
        data = response.json()
        response = requests.get(url=REVIEW_HOST + '/users/%d/reviews/' % pk)
        reviews = response.json()
        response = requests.delete(url=REVIEW_HOST + '/users/%d/reviews/' % pk)
        for review in reviews:
            response = requests.get(
                url=REVIEW_HOST + '/movies/{}/rating'.format(review['movie_id'])
            )
            new_rating = response.json()['rating'] or 0

            response = requests.put(
                url=MOVIE_HOST + '/movies/{}'.format(review['movie_id']),
                data={'rating': new_rating},
            )
        response = requests.delete(url=REVIEW_HOST + '/users/%d/reviews/' % pk)
        # if response.status_code != 200: do smths
        return Response(data=data, status=status.HTTP_200_OK)


class UserAllView(APIView):
    def get(self, request):
        response = requests.get(url=USER_HOST + '/users/')
        return Response(data=response.json(), status=response.status_code)

    def post(self, request):
        response = requests.post(url=USER_HOST + '/users/', data=request.data)
        return Response(data=response.json(), status=response.status_code)


class MovieView(APIView):
    def get(self, request, pk):
        response = requests.get(url=MOVIE_HOST + '/movies/%d' % pk)
        return Response(data=response.json(), status=response.status_code)

    def put(self, request, pk):
        response = requests.put(url=MOVIE_HOST + '/movies/%d' % pk, data=request.data)
        return Response(data=response.json(), status=response.status_code)

    def delete(self, request, pk):
        response = requests.delete(url=MOVIE_HOST + '/movies/%d' % pk)
        if response.status_code != status.HTTP_200_OK:
            return Response(data=response.json(), status=response.status_code)
        data = response.json()
        response = requests.delete(url=REVIEW_HOST + '/movies/%d/reviews/' % pk)
        # if response.status_code != 200: do smths
        return Response(data=data, status=status.HTTP_200_OK)


class MovieAllView(APIView):
    def get(self, request):
        response = requests.get(
            url=MOVIE_HOST + '/movies/',
            params={
                'page': request.GET.get('page', None),
                'limit': request.GET.get('limit', None)
            }
        )
        data = response.json()
        if response.status_code == status.HTTP_200_OK:
            data.update({'next': make_pagination_url(request, data['next'])})
            data.update({'previous': make_pagination_url(request, data['previous'])})
        return Response(data=data, status=response.status_code)

    def post(self, request):
        response = requests.post(url=MOVIE_HOST + '/movies/', data=request.data)
        return Response(data=response.json(), status=response.status_code)


class ReviewView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', None)
        movie_id = request.data.get('movie_id', None)
        if user_id is None or movie_id is None:
            return Response(
                {"message:": "Some fields not found:("},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = requests.get(
            url=USER_HOST + '/users/{}'.format(user_id)
        )
        if response.status_code != status.HTTP_200_OK:
            return Response({"message": "User with ID {} does not exist".format(user_id)})

        response = requests.get(
            url=MOVIE_HOST + '/movies/{}'.format(movie_id)
        )
        if response.status_code != status.HTTP_200_OK:
            return Response({"message": "Movie with ID {} does not exist".format(movie_id)})
        response = requests.post(url=REVIEW_HOST + '/reviews/', data=request.data)

        data = response.json()
        movie_id = request.data['movie_id']
        response = requests.get(
            url=REVIEW_HOST + '/movies/{}/rating'.format(movie_id)
        )
        new_rating = response.json()['rating'] or 0

        response = requests.put(
            url=MOVIE_HOST + '/movies/{}'.format(movie_id),
            data={'rating': new_rating},
        )
        return Response(data=data, status=status.HTTP_200_OK)

    def put(self, request):
        response = requests.put(url=REVIEW_HOST + '/reviews/', data=request.data)
        if response.status_code != status.HTTP_200_OK:
            return Response(data=response.json(), status=response.status_code)
        data = response.json()

        movie_id = request.data['movie_id']
        response = requests.get(
            url=REVIEW_HOST + '/movies/{}/rating'.format(movie_id)
        )
        new_rating = response.json()['rating']

        response = requests.put(
            url=MOVIE_HOST + '/movies/{}'.format(movie_id),
            data={'rating': new_rating},
        )
        return Response(data=data, status=status.HTTP_200_OK)


class ReviewMovieView(APIView):
    def get(self, request, movie_id):
        response = requests.get(
            url=REVIEW_HOST + '/movies/%d/reviews/' % movie_id,
            params={
                'page': request.GET.get('page', None),
                'limit': request.GET.get('limit', None)
            }
        )
        data = response.json()
        if response.status_code == status.HTTP_200_OK:
            data.update({'next': make_pagination_url(request, data['next'])})
            data.update({'previous': make_pagination_url(request, data['previous'])})

        reviews = data['results']
        user_ids = ','.join([str(rev["user_id"]) for rev in reviews])
        response_users = requests.get(
            url=USER_HOST + '/users/',
            params = {'ids': user_ids}
        )
        users = response_users.json()['users']
        for review in reviews:
            for user in users:
                if review['user_id'] == user['id']:
                    review['username'] = user['username']
        data['results'] = reviews

        return Response(data=data, status=response.status_code)


class UserMovieReview(APIView):
    def get(self, request, user_id, movie_id):
        response = requests.get(
            url=REVIEW_HOST + '/users/{}/reviews/movies/{}'.format(user_id, movie_id)
        )
        return Response(data=response.json(), status=response.status_code)
