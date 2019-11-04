from django.db import models


class Usuario(models.Model):
    nombre                  = models.CharField(max_length = 50)
    usuario                 = models.CharField(max_length = 50, unique=True)
    rol                     = models.CharField(max_length = 50)
    identificador           = models.CharField(max_length = 250)
    foto_perfil             = models.FileField(upload_to="foto_perfil", max_length=100)
    estaHabilitado          = models.BooleanField(default=True)
    estado                  = models.CharField(max_length = 250)
    correo                  = models.CharField(max_length = 50, unique=True)
    contraseña              = models.CharField(max_length = 250)
    listaContactos          = models.ManyToManyField("self", blank=True) 

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def authenticate(self, usuario, contraseña):
        usuario = Usuario.objects.get(usuario= usuario, contraseña=contraseña)
        if not usuario:
            raise serializers.ValidationError({'error': 'Usuario no existe'},
                            status=HTTP_404_NOT_FOUND)
        return usuario
