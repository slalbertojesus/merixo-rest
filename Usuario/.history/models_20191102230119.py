from django.db import models
from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver  
from rest_framework.authtoken.models import Token  
import django.db.models.deletion

class Usuario(models.Model):
    nombre                  = models.CharField(max_length = 50, on_delete=models.CASCADE)
    USERNAME_FIELD          = models.CharField(max_length = 50, on_delete=models.CASCADE)
    rol                     = models.CharField(max_length = 50, on_delete=models.CASCADE)
    identificador           = models.CharField(max_length = 250, on_delete=models.CASCADE)
    foto_perfil             = models.FileField(upload_to="foto_perfil", max_length=100, on_delete=models.CASCADE)
    estaHabilitado          = models.BooleanField(default=True, on_delete=models.CASCADE)
    estado                  = models.CharField(max_length = 250, on_delete=models.CASCADE)
    correo                  = models.CharField(max_length = 50, unique=True, on_delete=models.CASCADE)
    contraseña              = models.CharField(max_length = 250, on_delete=models.CASCADE)
    listaContactos          = models.ManyToManyField("self", blank=True, on_delete=models.CASCADE) 

    REQUIRED_FIELDS = ['usuario', 'contraseña', 'nombre', 'correo', 'contraseñaConfirmacion', 'rol']

    def __str__(self):
        return self.usuario

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created: 
        Token.objects.create(Usuario = instance)
  