from django.urls import path
from .views import (
    UserAllView,
    UserView,
    UserMovieReview,
    MovieAllView,
    MovieView,
    ReviewMovieView,
    ReviewView,
)

urlpatterns = [
    path('users/', UserAllView.as_view()),
    path('users/<int:pk>', UserView.as_view()),
    path('users/<int:user_id>/reviews/movies/<int:movie_id>', UserMovieReview.as_view()),
    path('movies/<int:pk>', MovieView.as_view()),
    path('movies/<int:movie_id>/reviews/', ReviewMovieView.as_view()),
    path('movies/', MovieAllView.as_view()),
    path('reviews/', ReviewView.as_view()),
]