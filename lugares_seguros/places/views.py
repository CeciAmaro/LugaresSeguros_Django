from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from lugares_seguros.places.serializers import UserSingUpSerializer
from places.models import Place #modelo
from places.serializers import PlaceSerializer, UserSingUpSerializer #serializer


# Create your views here.

class PlaceView(APIView):
    def get(self, request):
        '''QuerySet --> Resultado de una Query. Lista de objetos'''
        places = Place.objects.all() #permite traer uno o muchos objetos
        print(places)
        serializer = PlaceSerializer(places, many=True) #resultado de la invocacion en un JSON
        return Response(serializer.data, status=status.HTTP_200_OK)
#crear un nuevo lugar 
    def post(self, request):
        serializer = PlaceSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True) #a la informacion almacenada en serializer se valida
        serializer.save() #se guarda la informacion en la base de datos
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PlaceSingleView(APIView):
    def put(self, request, id):
        place = Place.objects.get(id=id)
        serializer = PlaceSerializer(place, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response(serializer.data, status=status.HTTP_200_OK) 

    def delete(self, request, id): 
        place = Place.objects.get(id=id)
        place.delete()
        return Response({'message':'Lugar eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT) 


#registro
class UserSignUpView(APIView):
    def post(self, request):
        serializer = UserSingUpSerializer(data=request.data) #recibe la peticion
        serializer.is_valid(raise_exception=True)
        serializer.save() #guarda la informacion 
        return Response(serializer.data, status=status.HTTP_200_OK)


    
