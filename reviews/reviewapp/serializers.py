from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    movie_id = serializers.IntegerField()
    rating = serializers.FloatField()
    content = serializers.CharField(required=False)

    def validate_rating(self, value):
        return value

    def create(self, validate_data):
        return Review.objects.create(**validate_data)

    def update(self, instance, validate_data):
        instance.rating = validate_data.get('rating', instance.rating)
        instance.content = validate_data.get('content', instance.content)
        instance.save()

        return instance
