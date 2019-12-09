from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from django.utils.text import slugify
from django.core import serializers
from django.http import HttpResponse
from django.db import IntegrityError

import json
import requests

from Usuario.models import Account
from .models import Story
from .models import Like

from Usuario.serializers import AccountFavoritesSerializers
from .serializers import StoryCreateSerializer, StoriesSerializer, StoryCommentsSerializer

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
				try:
					account = serializer.save() 
					data['response'] = "se registró de forma exitosa"
					return Response(data, status=status.HTTP_201_CREATED)
				except IntegrityError:
					data['response'] = "Intente otro nombre"
					return Response(data, status=status.HTTP_409_CONFLICT)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Elimina una historia
# Permite eliminar una cuenta ligada a una historia
# Url: http://merixo.tk/<id>/delete
# Headers: Authorization: Token <token>
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def api_delete_story_view(request, id):
	try:
		story = Story.objects.get(id=id)
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

# Obtiene lista de historias de usuario
# Permite obtener lista de histori}as de usuario
# Url: http://merixo.tk/getallstories
# Headers: Authorization: Token <token>
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_get_all_stories_view(request):
	try:
		account = request.user.pk
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		account_storys = Story.objects.filter(author = account)
		serializer = StoriesSerializer(account_storys, many=True)
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Agrega historia a favoritos
# Permite agregar una historia a favoritos
# Url: http://merixo.tk/addtofavorites
# Headers: Authorization: Token <token>
@api_view(['PUT',]) 
@permission_classes((IsAuthenticated,))
def api_add_story_favorites_view(request):
	try:
		account = request.user
		storytoadd=request.POST.get('id')
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		usuario = Account.objects.get(username = account.username)
		usuario.historias_favoritos.append(storytoadd)
		usuario.save()
		data = {}
		data['response'] = "se agregó historia a lista de favoritos de forma exitosa"
		data[SUCCESS] = UPDATE_SUCCESS
		return Response(data=data)
	return Response(status=status.HTTP_400_BAD_REQUEST)
	
# Eliminar historia de favoritos
# Permite eliminar una historia de favoritos
# Url: http://merixo.tk/deletefromfavorites
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_delete_from_favorites_view(request):
	try:
		account = request.user
		storytodelete_req = request.POST.get('id')
		storytodelete = int(storytodelete_req)
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		usuario = Account.objects.get(username = account.username)
		usuario.historias_favoritos.remove(storytodelete)
		usuario.save()
		data = {}
		data['response'] = "se eliminó historia de favoritos de forma exitosa"
		data[SUCCESS] = UPDATE_SUCCESS
		return Response(data=data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Obtiene lista de historias en favoritos
# Permite obtener lista de historias de favoritos
# Url: http://merixo.tk/getfavstories
# Headers: Authorization: Token <token>
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_get_fav_stories_view(request):
	try:
		account = request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		usuario = Account.objects.get(username = account.username)
		favorites = usuario.historias_favoritos
		result = []
		item = 0
		identity = 0
		for item in favorites:
			story = Story.objects.get(id = favorites[identity])
			result.append(story)
			identity +=1
		serializer = StoriesSerializer(result, many=True)
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Obtiene lista de historias de contactos
# Permite obtener lista de historias de contactos agregados
# Url: http://merixo.tk/getfeed
# Headers: Authorization: Token <token>
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_get_feed_view(request):
	try:
		account = request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		usuario = Account.objects.get(username = account.username)
		contacts = usuario.listaUsuarios
		result = []
		user = 0
		username = 0
		story = 0
		for user in contacts:
			try:
				author_object = Account.objects.get(username = contacts[username])
			except author_object.DoesNotExist:
				pass
			else:
				try:
					user_storys = Story.objects.filter(author = author_object)
				except user_storys.DoesNotExist:
					username +=1
				else:
					for story in user_storys:
						result.append(story)
					username +=1
		serializer = StoriesSerializer(result, many=True)
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Añade comentario a historia
# Permite añadir un comentario a historia
# Url: http://merixo.tk/addcomment
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_add_comment_view(request):
	try:
		account = request.user
		story_id = request.POST.get('id')
		comment = request.POST.get('comment')
		if not comment:
			return Response(status=status.HTTP_404_NOT_FOUND)
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		data = {}
		try:
			story = Story.objects.get(id = story_id)
			story.comments.append(comment)
		except ValueError:
			return Response(status=status.HTTP_404_NOT_FOUND)
		story.save()
		data['response'] = "se agregó comentario de forma exitosa"
		data	[SUCCESS] = UPDATE_SUCCESS
		return Response(data=data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Obtiene lista de comentarios de historia
# Permite obtener lista de comentarios agregados a una historia
# Url: http://merixo.tk/getcomments
# Headers: Authorization: Token <token>
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_get_story_comments_view(request):
	try:
		account = request.user
		story_id = request.POST.get('id')
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		story = Story.objects.get(id = story_id)
		serializer = StoryCommentsSerializer(story)
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Dar like a historia
# Permite agregar un like a historia
# Url: http://merixo.tk/addlike
# Headers: Authorization: Token <token>
@api_view(['PUT',]) 
@permission_classes((IsAuthenticated,))
def api_add_like_view(request):
	try:
		account = request.user
		story_id=request.POST.get('id')
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		account = Account.objects.get(username = account.username)
		story = Story.objects.get(id = story_id)
		try:
			like = Like.objects.get(from_account = account, story = story).first()
		except Like.DoesNotExist:
			like = Like.objects.create(from_account = account, story = story)
			data = {}
			data['response'] = "se agregó like a historia de forma exitosa"
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		except Like.MultipleObjectsReturned:
				return Response(status=status.HTTP_409_CONFLICT)
	return Response(status=status.HTTP_400_BAD_REQUEST)