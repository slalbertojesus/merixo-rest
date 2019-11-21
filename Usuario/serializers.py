import os
from rest_framework import serializers
from .utils import StringArrayField
from django.db import models
from .models import Account
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from rest_framework.fields import ListField

from Usuario.utils import is_image_aspect_ratio_valid, is_image_size_valid
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class AccountAddUserSerializer(serializers.ModelSerializer):
	#listaUsuarios = StringArrayField()

	class Meta:
		model = Account
		fields = ['username']


class AccountLoginSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['name', 'email', 'username', 'estado']


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['name', 'email', 'username', 'estado', 'pic']

	def	save(self):
		account = Account(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			name=self.validated_data['name'],
			estado=self.validated_data['estado'],
			)
		account.save()
		return account

class AccountUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Account
		fields = ['name','estado','pic']

	def validate(self, account):
		try:
			pic = account['pic']
			url = os.path.join(settings.TEMP , str(pic))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in pic.chunks():
					destination.write(chunk)
				destination.close()
			
			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
					os.remove(url)
					raise serializers.ValidationError({"response": 
				"Imagen es muy grande"})
			
			if not is_image_aspect_ratio_valid(url):
					os.remove(url)
					raise serializers.ValidationError({"response": 
				"Altura de la imagen es inválida"})
			os.remove(url)
		except KeyError:
				pass
		return account

class AccountActivateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['is_active']

class RegistrationSerializer(serializers.ModelSerializer):

	passwordConfirm = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = Account
		fields = ['email', 'username', 'password', 'passwordConfirm', 'name']
		extra_kwargs = {
				'password': {'write_only': True},
		}	

	def update(self, instance, validated_data):
		account = Account(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			name=self.validated_data['name'],
			estado=self.validated_data['estado'],
			)
		if RegistrationSerializer.is_valid():
			RegistrationSerializer.update(instance=instance.account)
		return super(RegistrationSerializer, self).update(instance, validated_data)

	def	save(self):
		account = Account(
			email=self.validated_data['email'],
			username=self.validated_data['username'],
			name=self.validated_data['name'],
			)
		password = self.validated_data['password']
		passwordConfirm = self.validated_data['passwordConfirm']
		if password != passwordConfirm:
			raise serializers.ValidationError({'password': 'Contraseñas no son iguales.'})
		account.set_password(password)
		account.save()
		return account