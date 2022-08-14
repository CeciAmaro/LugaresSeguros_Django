from dataclasses import field, fields
from rest_framework import serializers
from .models import Comentario, Place, User

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

'''
class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguro
        fields = '__all__'
'''


#registro
'''
class UserSingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name",
        "username",
        "password",
        "is_active",
        "is_verified",
        "created_at",
        "update_at"]
'''
class UserSingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#cambio de contraseña
class RequestPasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=10)
    redirect_url = serializers.CharField(max_length=500, required=False)
    class Meta:
        fields=['email']

class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length =8, max_length = 20, write_only = True)

    class Meta:
        model = User
        fields = ['password', 'is_active']

    def validate(self, data):
        user = User(**data)
        password = data.get('password')
        min_length = 8
        max_length = 20 
        if len(password) < min_length or len(password) > max_length:
            raise serializers.ValidationError("La nueva contraseña de tener minimo 8 caracteres y maximo 20")

        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Debe tener al menos un letra mayuscula")

        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Debe tener al menos un letra minuscula")

        if not any(char in ['$', '@', '#', '%', '&', '!'] for char in password):
            raise serializers.ValidationError("Debe tener algun caracter especial")

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Debe tener algun numero")

        else: return data

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]