from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField()
    email = serializers.EmailField()

    def update(self, instance, validate_data):
        instance.username = validate_data.get('username', instance.username)
        instance.email = validate_data.get('email', instance.email)
        instance.save()
        return instance


class UserPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validate_data):
        return User.objects.create(**validate_data)

    def validate_username(self, value):
        return value

    def validate_email(self, value):
        return value

    def validate_password(self, value):
        return value

    def check_existing(self):
        pass
