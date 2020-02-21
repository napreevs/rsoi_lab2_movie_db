from django.urls import path
from .views import ReviewView, ReviewUserView, ReviewMovieView, RatingMovieView, ReviewUserMovieView

urlpatterns = [
    path('reviews/', ReviewView.as_view(), name='reviews'),
    path('users/<int:user_id>/reviews/', ReviewUserView.as_view(), name='user_reviews'),
    path('users/<int:user_id>/reviews/movies/<int:movie_id>', ReviewUserMovieView.as_view(), name='user_movie_review'),
    path('movies/<int:movie_id>/reviews/', ReviewMovieView.as_view(), name='movie_reviews'),
    path('movies/<int:movie_id>/rating', RatingMovieView.as_view(), name='movie_rating'),
]
