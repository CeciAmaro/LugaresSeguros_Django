#from urllib import response
#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from places.models import Place, User, Comentario #modelo
from places.serializers import PlaceSerializer, UserSingUpSerializer, ComentarioSerializer, RequestPasswordResetSerializer, SetNewPasswordSerializer, UserLoginSerializer #serializer
from rest_framework_simplejwt.tokens import RefreshToken
#from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
#from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.permissions import AllowAny

import jwt

JWT_authenticator = JWTAuthentication()
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 20


# Generates tokens manually.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

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

class ComentarioView(APIView):
    def post(self, request):
        serializer = ComentarioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        '''QuerySet --> Resultado de una Query. Lista de objetos'''
        comentario = Comentario.objects.all() #permite traer uno o muchos objetos
        #print(places)
        serializer = ComentarioSerializer(comentario, many=True) #resultado de la invocacion en un JSON
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class EliminarComentarioView(APIView):
    def delete(self, request, id): 
        comentario = Comentario.objects.get(id=id)
        comentario.delete()
        return Response({'message':'Comentario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)

#registro
class UserSignUpView(APIView):
    def post(self, request):
        serializer = UserSingUpSerializer(data=request.data) #recibe la peticion
        serializer.is_valid(raise_exception=True)
        serializer.save() #guarda la informacion 
        return Response(serializer.data, status=status.HTTP_200_OK)

class UsersListView(APIView):
    def get(self,request):
        users = User.objects.all()
        serializer = UserSingUpSerializer(users, many=True)
        return Response(serializer.data, status= status.HTTP_200_OK)

#editar perfil
class UpdatePerfilView(APIView):
    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSingUpSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return  Response(serializer.data, status=status.HTTP_200_OK)

#cambio de contraseña 
#solita el correo electronico de reestablecimiento de contrseña
class RequestPasswordResetEmail(APIView):
    serializer = RequestPasswordResetSerializer
    def post(self, request):
        serializer = self.serializer(data=request.data)
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse('restablecimiento-completo')
            absurl = 'http://'+current_site + relativeLink+"?token="+str(refresh)
            email_body = 'Hola'+user.email+'utiliza este enlace para cambiar tu contraseña \n'+absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'cambio de contraseña'}
            Util.send_email(data)
            print(user)
            return Response({'message': 'Te hemos enviado un enlace para restablecer tu contraseña'}, status= status.HTTP_200_OK)
            
        else:
            return Response({'message': 'No puede colocar un usuario que no existe'})

    
#verificacion de token de la contraseña
class SetNewPasswordView(APIView):
    def patch(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={"verify_signature": False}, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('No autorizado')
        user =User.objects.filter(id=payload['user_id']).first()
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data['password']
        else:
            return Response({'message': 'La contraseña debe tener los requerimientos'})
        return Response({'sucess': True, 'message': 'Ya se a restablecido'}, status=status.HTTP_200_OK)


#login
class LoginView(APIView):
    permissions_classes = (AllowAny,)
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response({'status':404, 'message':'User not found'})
            
        if not user.is_verified:
            return Response({'status':401, 'message':'Account is not verified'})
            
        user.save()

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.data = {
				'access': str(refresh.access_token),
				'refresh': str(refresh), 
				'status': 200,
				'id': user.id
			}
            
        return response
    
    





    