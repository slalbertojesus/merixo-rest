from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Usuario
from .serializers import UsuarioSerializer

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'

@api_view(['GET', ])
def detalles_usuario_view(request, identificador):

	try:
		usuario = Usuario.objects.get(identificador = identificador)
	except usuario.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == 'GET':
		serializer = UsuarioSerializer(usuario)
		return Response(serializer.data)