from rest_framework import serializers

from django.db import models

from .models import Usuario

class UsuarioSerializer(models.Model):

    contraseñaConfirmacion = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = Usuario
        fields = ['usuario', 'contraseña', 'nombre', 'correo', 'contraseñaConfirmacion']
        

    def save(self):
        usuario = Usuario(
            usuario = self.validated_data['usuario'],
            correo = self.validated_data['correo'],
        )
        contraseña = self.validated_data['contraseña']
        contraseñaConfirmacion = self.validated_data['contraseñaConfirmacion']
        if contraseña != contraseñaConfirmacion: 
            raise serializers.ValidationError({'contraseña': 'Las contraseñas no son iguales'})
        usuario.set_password(contraseña)
        usuario.save()
        return usuario

