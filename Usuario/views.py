from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from django_postgres_extensions.models.functions import ArrayAppend
import json

from .models import Account
from .serializers import RegistrationSerializer, AccountSerializer, AccountUpdateSerializer, AccountContactsSerializers

SUCCESS = 'exito'
ERROR = 'error'
DELETE_SUCCESS = 'Eliminado'
UPDATE_SUCCESS = 'Actualizado'
CREATE_SUCCESS = 'Creado'

# Obtiene propiedades de cuenta
# Obtiene las propiedades: name, email, username , estado, pic del objeto Account
# Url: https://merixo.tk/peroperties
# Headers: Authorization: Token <token>
@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_usuario_view(request):
	try:
		account = request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'GET':
		serializer = AccountSerializer(account)
		return Response(serializer.data)	

# Actualiza cuenta
# Permite actualizar las propiedades de la cuenta
# Url: https://merixo.tk/peroperties/update
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_usuario_view(request):
	try:
		account = request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		serializer = AccountUpdateSerializer(account, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "se actualizó información de forma exitosa"
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Añade contacto
# Permite añadir un contacto a la cuenta del usuario
# Url: http://merixo.tk/addcontact
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_add_user_view(request):
	try:
		account = request.user
		usertoadd=request.POST.get('usertoadd')
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		usuario = Account.objects.get(username = account.username)
		usuario.listaUsuarios.append(usertoadd)
		usuario.save()
		data = {}
		if usuario.exists():
			data['response'] = "se agregó contacto de forma exitosa"
			data	[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Eliminar contacto
# Permite eliminar un contacto de la cuenta del usuario
# Url: http://merixo.tk/deletecontact
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_delete_user_view(request):
	try:
		account = request.user
		usertodelete=request.POST.get('usertodelete')
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		usuario = Account.objects.get(username = account.username)
		usuario.listaUsuarios.remove(usertodelete)
		usuario.save()
		data = {}
		if usuario.exists():
			data['response'] = "se eliminó contacto de forma exitosa"
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(status=status.HTTP_400_BAD_REQUEST)

# Obtiene contactos
# Permite obtener todos los contactos de la cuenta del usuario.
# Url: http://merixo.tk/getallcontacts
# Headers: Authorization: Token <token>
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def api_get_all_contacts_user_view(request):
	try:
		account = request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		usuario = Account.objects.get(username = account.username)
		serializer = AccountContactsSerializers(usuario)
		return Response(serializer.data)
	return Response(status=status.HTTP_400_BAD_REQUEST)

# Desactiva usuario
# Desactiva una cuenta de usuario
# Url: http://merixo.tk/properties/delete
# Headers: Authorization: Token <token>
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def api_delete_usuario_view(request):
	try:
		account = request.user
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		serializer = AccountUpdateSerializer(account, data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = "se actualizó estado de forma exitosa"
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Crea una cuenta
# Permite añadir una cuenta 
# Url: http://merixo.tk/create
@api_view(['POST',])
@permission_classes([AllowAny,])
def api_create_usuario_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializer(data=request.data)
		data = {}
		if serializer.is_valid():
			account = serializer.save() 
			data['response'] = "se registró de forma exitosa"
			data['email'] = account.email
			data['username'] = account.username
			token = Token.objects.get(user = account).key
			data['token'] = token
			return Response(data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Iniciar sesión
# Permite iniciar sesión en el sistema
# Url: http://merixo.tk/login
@api_view(['POST',])
@permission_classes([AllowAny,])
def api_sing_up_usuario_view(request):
	if request.method == 'POST':
		data = {}
		account = authenticate(
		request, 
		username=request.POST.get('email'), 
		password=request.POST.get('password'))
	if account:
		try:
			token = Token.objects.get(user=account)
			data['response'] = 'Se ha ingresado'
			data['username'] = account.username
			data['email'] = account.email
			data['name'] = account.name
			data['estado'] = account.estado
			data['token'] = token.key
			return Response(data, status=status.HTTP_201_CREATED)
		except Token.DoesNotExist:
			token = Token.objects.create(user=account)
	else:
		data['response'] = 'Error' 
		data['error_message'] = 'Datos inválidos'
		return Response(data)
	return Response(status=status.HTTP_400_BAD_REQUEST)