from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer, RegistrationSerializer)


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                {
                    'data': serializer.errors,
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {
                'data': serializer.data,
                'success': True
            }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                'data': serializer.data,
                'success': True
            }, status=status.HTTP_200_OK
        )
