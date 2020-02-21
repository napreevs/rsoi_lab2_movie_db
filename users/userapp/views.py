from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from aldjemy.core import get_engine
from sqlalchemy.sql import select
from .models import User
from .serializers import UserSerializer, UserPasswordSerializer

engine = get_engine()


def str_to_int_list(ids):
    ids = ids.split(',')
    res = []
    for id in ids:
        try:
            res.append((int(id)))
        except ValueError:
            return []
    return res


# Create your views here.
class UserView(APIView):
    def get(self, request):
        ids = request.GET.get('ids', None)
        if ids:
            ids = str_to_int_list(ids)
            if not ids:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            users = User.objects.filter(pk__in=ids)
        else:
            users = User.objects.all()
        serialized = UserSerializer(users, many=True)
        return Response({"users": serialized.data})

    def post(self, request):
        serialized = UserPasswordSerializer(data=request.data)
        if serialized.is_valid():
            try:
                created_user = serialized.save()
            except IntegrityError:
                return Response({"message": "Username/email is already taken."}, status=status.HTTP_409_CONFLICT)
            return Response(UserSerializer(created_user).data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        serialized = UserSerializer(user)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response({"message": "Username/email is already taken."}, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        user.delete()

        return Response({"message": "User '{}' was removed".format(pk)},
                        status=status.HTTP_200_OK)
