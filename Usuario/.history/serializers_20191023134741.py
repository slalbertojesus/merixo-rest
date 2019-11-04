from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):

    contraseñaConfirmacion = serializers.CharField(style={'input_type':'password'}, write_only= True)

    class Meta:
        model = Usuario
        fields = ('usuario', 'contraseña', 'nombre', 'correo', 'contraseñaConfirmacion')
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def save(self):
        usuario = Usuario(
            usuario = self.validated_data['usuario'],
            correo = self.validated_data['correo'],
        )
        contraseña = self.validated_data['contraseña']
        contraseñaConfirmacion = self.validated_data['passwordConfirmacion']
        if contraseña != contraseñaConfirmacion: 
            raise serializers.ValidationError({'contraseña': 'Las contraseñas no son iguales'})
        usuario.set_password(contraseña)
        usuario.save()
        return usuario

