from rest_framework import serializers
from .models import Movie, MovieFeature, Feature


class MovieSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField()
    release_year = serializers.IntegerField()
    director = serializers.CharField()
    writer = serializers.CharField()
    genre = serializers.CharField()
    description = serializers.CharField()
    country = serializers.CharField()
    rating = serializers.FloatField(required=False)
    box_office = serializers.IntegerField()

    def update(self, instance, validate_data):
        instance.title = validate_data.get('title', instance.title)
        instance.release_year = validate_data.get('release_year', instance.release_year)
        instance.director = validate_data.get('director', instance.director)
        instance.writer = validate_data.get('writer', instance.writer)
        instance.genre = validate_data.get('genre', instance.genre)
        instance.description = validate_data.get('description', instance.description)
        instance.country = validate_data.get('country', instance.country)
        instance.rating = validate_data.get('rating', instance.rating)
        instance.box_office = validate_data.get('box_office', instance.box_office)
        instance.save()

        return instance

    def create(self, validate_data):
        return Movie.objects.create(**validate_data)

    def validate_name(self, value):
        return value


class MovieInfoSerializer(MovieSerializer):
    features = serializers.SerializerMethodField()

    def get_features(self, obj):
        title = list(filter(None, obj.feature_name))
        description = list(filter(None, obj.feature_description))
        if len(obj.feature_name) == 0 or len(title) != len(description):
            return []
        return [{"feature": title, "description": des} for title, des in zip(title, description)]

    class Meta:
        ordering = ['-id']


class MovieFeatureSerializer(serializers.Serializer):
    movie_id = serializers.IntegerField()
    feature_id = serializers.IntegerField()
    description = serializers.CharField()

    def validate_feature_id(self, value):
        return value

    def create(self, validate_data):
        movie = Movie.objects.get(id=validate_data['movie_id'])
        feature = Feature.objects.get(id=validate_data['feature_id'])
        return MovieFeature.objects.create(
            movie=movie, feature=feature, description=validate_data['description']
        )
