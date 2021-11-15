from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import SwiperContent
from .serializers import SwiperContentSerializer

@api_view(['GET'])
def helloAPI(request):
    return Response("hello world!")