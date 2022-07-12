from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.

'''
def index(request):
    return HttpResponse("Hello, world. Desde una view")
    '''

class HelloDrf(APIView):
    def get(self, request, format=None):
        return Response({"message": 'Hello world DRF'})
    

