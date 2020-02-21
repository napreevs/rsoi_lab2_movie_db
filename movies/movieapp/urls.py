from django.urls import path
from .views import MovieView, MovieDetailView, MovieFeatureView, FeatureView

urlpatterns = [
    path('movies/', MovieView.as_view(), name='get_post_movies'),
    path('movies/<int:pk>', MovieDetailView.as_view(), name='get_put_delete_movies'),
    path('movies/<int:movie_id>/features/', MovieFeatureView.as_view(), name='post_moviefeatures'),
    path('features/', FeatureView.as_view(), name='post_features')
]
