from rest_framework.decorators import api_view
from rest_framework.response import Response
from.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#Se logean los usuarios
@api_view(['POST'])
def login(request):

    #Busca en la base de datos segun el username si no es encontrado arrojara error
    user =get_object_or_404(User, username=request.data['username'])
    #Si la contrase;a es erronea arrojara un error
    if not user.check_password(request.data['password']):
        return Response({"error":"Contraseña Invalida"}, status=status.HTTP_400_BAD_REQUEST)
    #Guardamos u obtenemos el token
    token, created=Token.objects.get_or_create(user=user)
    #Serializamos el objeto user, para poder asi ser enviados
    serializer=UserSerializer(instance=user)

    return Response({"token":token.key, "user":serializer.data},status=status.HTTP_200_OK)

#Crean usuarios
@api_view(['POST'])
def register(request):
    #Se encarga de validar los datos recibidos
    serializer= UserSerializer(data=request.data) 

    if serializer.is_valid():

        #Se guardan los datos en la BD
        serializer.save()
        #Se llaman los datos
        user= User.objects.get(username=serializer.data['username'])
        #Se guarda la contrase;a de con hash 
        user.set_password(serializer.data['password'])
        #Se guarda nuevamente el objeto en la BD
        user.save()
        #Se crea un token asociado al usuario 
        token= Token.objects.create(user=user)

        return Response({'token': token.key, "user":serializer.data}, status=status.HTTP_201_CREATED)


    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Visualizamos los datos del usuario en sesión
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    #Serializamos los datos del usuario que envia la solicitud para poder enviarlos
    serializer = UserSerializer(instance=request.user)
    
    return Response(serializer.data,status=status.HTTP_200_OK)