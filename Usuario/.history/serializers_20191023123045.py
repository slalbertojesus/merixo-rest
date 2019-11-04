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
                usuario = self.validated_data[-]
                correo = self.validated_data[]
            )

