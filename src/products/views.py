from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class Products(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        pass