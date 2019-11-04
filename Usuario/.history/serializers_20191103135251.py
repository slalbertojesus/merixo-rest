from rest_framework import serializers

from django.db import models

from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    passwordConfirm = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = Usuario
        fields = ['usuario', 'password', 'nombre', 'email', 'passwordConfirm', 'rol']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        usuario = Usuario(
            nombre = self.validated_data['nombre'],
            usuario = self.validated_data['usuario'],
            email = self.validated_data['email'],
            rol = "usuario"
        )
        password = self.validated_data['password']
        passwordConfirm = self.validated_data['passwordConfirm']
        if password != passwordConfirm: 
            raise serializers.ValidationError({'password': 'Las contraseñas no son iguales'})
        usuario.password = password
        usuario.save()
        return usuario

