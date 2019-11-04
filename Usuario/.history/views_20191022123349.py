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