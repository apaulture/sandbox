from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from restapp.models import Snippet
from restapp.serializers import SnippetSerializer
from restapp.serializers import *

class SnippetList(APIView):
    """
    List all code snippets, or create a new snippet.
    """
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)

    def get(self, request, format = None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many = True)
        return Response(serializer.data)

    def post(self, request, format = None):
        serializer = SnippetSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save() # perform_create is called here
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a code snippet.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk = pk)
        except Snippet.DoesNotExist:
            # return Response(status = status.HTTP_404_NOT_FOUND)
            raise Http404

    def get(self, request, pk, format = None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format = None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer