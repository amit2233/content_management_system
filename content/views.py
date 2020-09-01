from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Content
from .serializers import ContentSerializer


class ContentUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = Content.objects.filter(user=request.user)
        return Response(
            {
                'data': ContentSerializer(content, many=True).data,
                'success': True
            }, status=status.HTTP_200_OK
        )

    def post(self, request):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['user'] = request.user.id
        request.data._mutable = _mutable
        serializer = ContentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'data': serializer.errors,
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            {
                'data': serializer.data,
                'success': True
            }, status=status.HTTP_200_OK
        )

    def put(self, request):
        try:
            content = Content.objects.get(id=request.data.get('id'), user=request.user)
        except Content.DoesNotExist:
            return Response(
                {
                    'msg': 'Invalid Content Id',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ContentSerializer(data=request.data, instance=content, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'msg': "Invalid Data",
                    'data': serializer.errors,
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({'data': ContentSerializer(content).data}, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            content = Content.objects.get(id=request.GET.get('id'), user=request.user)
        except Content.DoesNotExist:
            return Response({'msg': 'Invalid Content Id'}, status=status.HTTP_400_BAD_REQUEST)

        content.delete()
        return Response(
            {
                'msg': "Deleted Successfully",
                'data': ContentSerializer(content).data,
                'success': True
            }, status=status.HTTP_200_OK)


class ContentAdminAPIView(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        content = Content.objects.all()
        return Response(
            {
                'data': ContentSerializer(content, many=True).data,
                'success': True
            }, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            content = Content.objects.get(id=request.data.get('id'))
        except Content.DoesNotExist:
            return Response(
                {
                    'msg': 'Invalid Content Id',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ContentSerializer(data=request.data, instance=content, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    'msg': "Invalid Data",
                    'data': serializer.errors,
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(
            {
                'msg': "Content Updated Successfully",
                'data': ContentSerializer(content).data,
                'success': True
            }, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            content = Content.objects.get(id=request.GET.get('id'))
        except Content.DoesNotExist:
            return Response(
                {
                    'msg': 'Invalid Content Id',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)

        content.delete()
        return Response(
            {
                'msg': "Deleted Successfully",
                'data': ContentSerializer(content).data,
                'success': True
            }, status=status.HTTP_200_OK)


class SearchAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = Content.objects.filter(
            Q(title__icontains=request.GET.get('search')) | Q(body__icontains=request.GET.get('search')) | Q(
                summary__icontains=request.GET.get('search')) | Q(category__icontains=request.GET.get('search'))
        )
        return Response(
            {
                'data': ContentSerializer(content, many=True).data,
                'success': True
            }, status=status.HTTP_200_OK
        )
