from django.shortcuts import render
from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer


@api_view(["POST"])
def CreateUserView(request):
    if request.method == "POST":
        data = request.data
        serializer = UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND
            )

        serializer.save()
        return Response(
            data=serializer.errors,
            status=status.HTTP_201_CREATED
        )