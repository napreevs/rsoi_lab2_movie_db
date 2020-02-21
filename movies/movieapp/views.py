from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import Movie, MovieInfo, Feature
from .serializers import MovieSerializer, MovieInfoSerializer, MovieFeatureSerializer
from .pagination import BasicPagination, PaginationHandlerMixin


# Create your views here.
class MovieView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination

    def get(self, request):
        # movies = MovieInfo.objects.all().order_by
        movies = Movie.objects.all().order_by('id')

        page = self.paginate_queryset(movies)
        if page is not None:
            serialized = self.get_paginated_response(
                # MovieInfoSerializer(page, many=True).data
                MovieSerializer(page, many=True).data

            )
        else:
            # serialized = MovieInfoSerializer(movies, many=True)
            serialized = MovieSerializer(movies, many=True)

        return Response(serialized.data)

    def post(self, request):
        serialized = MovieSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieDetailView(APIView):
    def get(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        serialized = MovieSerializer(movie)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        serializer = MovieSerializer(instance=movie, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = get_object_or_404(Movie.objects.all(), pk=pk)
        movie.delete()

        return Response({"message": "Movie # '{}' was removed".format(pk)}, status=status.HTTP_200_OK)


class FeatureView(APIView):
    def post(self, request):
        data = request.data
        title = data.get('title')
        if title is None or title == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        feature = Feature.objects.create(title=title)
        return Response({"id": feature.id, "title": feature.title}, status=status.HTTP_201_CREATED)


class MovieFeatureView(APIView):
    def post(self, request, movie_id):
        data = request.data
        data['movie_id'] = movie_id
        serializer = MovieFeatureSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
            except (Movie.DoesNotExist, Feature.DoesNotExist):
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_201_CREATED)