from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from .models import Usuario
from .serializers import UsuarioSerializer

SUCCESS = 'exito'
ERROR = 'error'
DELETE_SUCCESS = 'eliminado'
UPDATE_SUCCESS = 'actualizado'
CREATE_SUCCESS = 'creado'

@api_view(['GET', ])
def api_detail_usuario_view(request, identificador):
	try:
		usuario = Usuario.objects.get(identificador = identificador)
	except usuario.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = UsuarioSerializer(usuario)
		return Response(serializer.data)

@api_view(['PUT',])
def api_update_usuario_view(request, identificador):
	try:
		usuario = Usuario.objects.get(identificador = identificador)
	except usuario.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'PUT':
		serializer = UsuarioSerializer(usuario, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
def api_delete_usuario_view(request, identificador):
	try:
		usuario = Usuario.objects.get(identificador=identificador)
	except usuario.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		operation = usuario.delete()
		data = {}
		if operation:
			data[SUCCESS] = DELETE_SUCCESS
		return Response(data=data)


@api_view(['POST',])
@permission_classes([AllowAny,])
def api_create_usuario_view(request):
	if request.method == 'POST':
		serializer = UsuarioSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			usuario = serializer.save() 
			data['response'] = "se registró de forma exitosa"
			data['nombre'] = usuario.nombre
			data['usuario'] = usuario.usuario
			token = Token.objects.get(Usuario).key
			data['token'] = token
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny,])
def api_login(request):
    usuario = request.data.get("usuario")
    password = request.data.get("password")
    if usuario is None or password is None:
        return Response({'error': 'No existe contraseña ni usuario'},
                        status=HTTP_400_BAD_REQUEST)
    usuario = authenticate(usuario=usuario, password=password)
    get_tokens_for_user(usuario)
    return {
        'refresh': str(token),
        'access': str(token.access_token),
    }


def authenticate(usuario, password):
        usuario = Usuario.objects.get(usuario= usuario, password=password)
        if not usuario:
            raise serializers.ValidationError({'error': 'Usuario no existe'},
                            status=HTTP_404_NOT_FOUND)
        return usuario