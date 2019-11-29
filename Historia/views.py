from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from django.utils.text import slugify

from Usuario.models import Account
from .models import Story

from .serializers import StoryCreateSerializer

SUCCESS = 'exito'
ERROR = 'error'
DELETE_SUCCESS = 'Eliminado'
UPDATE_SUCCESS = 'Actualizado'
CREATE_SUCCESS = 'Creado'

# Crea una historia 
# Permite añadir una historia leigadaa a una cuenta
# Url: http://merixo.tk/createstory
# Headers: Authorization: Token <token>
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def api_create_story_view(request):
	if request.method == 'POST':
		data = request.data
		account = request.user.pk
		data['author'] = account
		serializer = StoryCreateSerializer(data=data)
		data = {}
		if serializer.is_valid():
			account = serializer.save() 
			data['response'] = "se registró de forma exitosa"
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Elimina una historia
# Permite eliminar una cuenta ligada a una historia
# Url: http://merixo.tk/<slug>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_story_view(request, slug):
	try:
		story = Story.objects.get(slug=slug)
	except story.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	user = request.user
	if story.author != user:
		return Response({'response':"No tienes permiso para eliminar esta historia."}) 
	if request.method == 'DELETE':
		operation = story.delete()
		data = {}
		if operation:
			data['response'] = DELETE_SUCCESS
		return Response(data=data)