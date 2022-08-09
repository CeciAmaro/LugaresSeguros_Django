from dataclasses import field, fields
from rest_framework import serializers
from .models import Place, User

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

#registro
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