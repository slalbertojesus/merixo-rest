from rest_framework import serializers

from django.db import models

from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    contraseñaConfirmacion = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = Usuario
        fields = ['usuario', 'contraseña', 'nombre', 'correo', 'contraseñaConfirmacion', 'rol']
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        usuario = Usuario(
            usuario = self.validated_data['usuario'],
            correo = self.validated_data['correo'],
            rol = "usuario"
        )
        contraseña = self.validated_data['contraseña']
        contraseñaConfirmacion = self.validated_data['contraseñaConfirmacion']
        if contraseña != contraseñaConfirmacion: 
            raise serializers.ValidationError({'contraseña': 'Las contraseñas no son iguales'})
        usuario.contraseña = contraseña
        usuario.save()
        return usuario

    def authenticate(usuario, contraseña):
        usuario = Usuario.objects.get(usuario= usuario, contraseña=contraseña)
        if not usuario:
            raise serializers.ValidationError({'error': 'Usuario no existe'},
                            status=HTTP_404_NOT_FOUND)
        return usuario

