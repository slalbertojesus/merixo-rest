from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('__all__')
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        usuario = Account(
            usuario = self.validated_data['usuario'],
            correo = self.validated_data['correo'],
        )
        contraseña = self.validated_data['password']
        contraseñaConfirmacion = self.validated_data['passwordConfirmacion']

        if contraseña != contraseñaConfirmacion: 
            raise serializers.ValidationError({'contraseña': 'Las contraseñas no son iguales'})
        usuario.set_password(contraseña)
        usuario.save()
        return usuario

