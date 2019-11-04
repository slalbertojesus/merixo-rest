from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Usuario
from .serializers import UsuarioSerializer

SUCCESS = 'exito'
ERROR = 'error'
DELETE_SUCCESS = 'eliminado'
UPDATE_SUCCESS = 'actualizado'
CREATE_SUCCESS = 'creado'

@api_view(['GET', ])
def api_detalles_usuario_view(request, identificador):
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
def api_usuario_blog_view(request, identificador):

	try:
		blog_post = Usuario.objects.get(identificador=identificador)
	except BlogPost.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'DELETE':
		operation = blog_post.delete()
		data = {}
		if operation:
			data[SUCCESS] = DELETE_SUCCESS
		return Response(data=data)


@api_view(['POST'])
def api_create_blog_view(request):

	account = Account.objects.get(pk=1)

	blog_post = BlogPost(author=account)

	if request.method == 'POST':
		serializer = BlogPostSerializer(blog_post, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)