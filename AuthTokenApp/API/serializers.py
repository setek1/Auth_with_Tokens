from rest_framework import serializers
from django.contrib.auth.models import User

#Ocupamos el model incorporador por django, User.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id', 'username', 'email', 'password']


