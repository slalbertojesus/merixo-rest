from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from registration.backends.hmac.views import RegistrationView as coso
from django.contrib.auth import authenticate 
from django_postgres_extensions.models.functions import ArrayAppend

from .models import Account
from .serializers import RegistrationSerializer, AccountSerializer, AccountUpdateSerializer, AccountAddUserSerializer

SUCCESS = 'exito'
ERROR = 'error'
DELETE_SUCCESS = 'Eliminado'
UPDATE_SUCCESS = 'Actualizado'
CREATE_SUCCESS = 'Creado'


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

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_add_user_view(request):
	try:
		account = request.user
		usertoadd=request.POST.get('usertoadd')
		username=request.POST.get('username')
	except account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'PUT':
		usuario = Account.objects.get(username = username)
		usuario.listaUsuarios.append(usertoadd)
		serializer = AccountAddUserSerializer(usuario, data=request.data)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "se agregó usuario de forma exitosa"
			data[SUCCESS] = UPDATE_SUCCESS
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['POST',])
@permission_classes([AllowAny,])
def api_sing_up_usuario_view(request):
	if request.method == 'POST':
		data = {}
		account = authenticate(
		request, 
		username=request.POST.get('email'), 
		password=request.POST.get('password')
		)

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
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

