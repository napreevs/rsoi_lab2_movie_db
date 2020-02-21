from django.shortcuts import render
from django.db import IntegrityError
from django.db.transaction import savepoint, savepoint_commit, savepoint_rollback
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from .models import Review
from .serializers import ReviewSerializer
from .paginator import BasicPagination, PaginationHandlerMixin


# Create your views here.
class ReviewView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serialized = ReviewSerializer(reviews, many=True)
        return Response({"reviews": serialized.data})

    def post(self, request):
        serialized = ReviewSerializer(data=request.data)
        if serialized.is_valid():
            try:
                serialized.save()
            except IntegrityError as err:
                return Response({"message": str(err)}, status=status.HTTP_409_CONFLICT)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if request.data.get("user_id") is None or request.data.get("movie_id") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        review = get_object_or_404(Review.objects.all(),
                                   user_id=request.data.get("user_id"),
                                   movie_id=request.data.get("movie_id"))
        serialized = ReviewSerializer(review, request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response({"some_error"}, status=status.HTTP_400_BAD_REQUEST)


class ReviewUserView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self, request, user_id):
        reviews = Review.objects.filter(user_id=user_id)
        serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data)

    def delete(self, request, user_id):
        reviews = Review.objects.filter(user_id=user_id)
        reviews.delete()
        return Response({"message": "all reviews on movie with ID {} were removed".format(user_id)})


class ReviewUserMovieView(APIView):
    def get(self, request, user_id, movie_id):
        reviews = Review.objects.filter(user_id=user_id, movie_id=movie_id)
        # if reviews.exists():
        serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data)
        # return Response({})


class ReviewMovieView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serialized = self.get_paginated_response(
                ReviewSerializer(page, many=True).data
            )
        else:
            serialized = ReviewSerializer(reviews, many=True)
        return Response(serialized.data)

    def delete(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        reviews.delete()
        return Response({"message": "all reviews on movie with ID {} were removed".format(movie_id)})


class RatingMovieView(APIView):
    def get(self, request, movie_id):
        avg = Review.objects.filter(movie_id=movie_id).aggregate(rating=Avg('rating'))
        print(avg)
        return Response(avg)
