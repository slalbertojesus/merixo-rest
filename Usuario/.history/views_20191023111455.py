from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permission import AllowAny

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


@api_view(['POST'])
def api_create_usuario_view(request, identificador):

	permission_classes	= (AllowAny,)

	try:
		usuario = Usuario.objects.get(identificador = identificador)
	except usuario.DoesNotExist:
		if request.method == 'POST':
			serializer = UsuarioSerializer(usuario, data=request.data)
			data = {}
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		