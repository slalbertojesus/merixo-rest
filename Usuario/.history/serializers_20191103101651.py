from rest_framework import serializers

from django.db import models

from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    passwordConfirm = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = Usuario
        fields = ['usuario', 'password', 'nombre', 'correo', 'passwordConfirm', 'rol']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        usuario = Usuario(
            usuario = self.validated_data['usuario'],
            correo = self.validated_data['correo'],
            rol = "usuario"
        )
        password = self.validated_data['password']
        contraseñaConfirmacion = self.validated_data['passwordConfirm']
        if password != passwordConfirm: 
            raise serializers.ValidationError({'password': 'Las contraseñas no son iguales'})
        usuario.password = password
        usuario.save()
        return usuario

