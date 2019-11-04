from django.db import models
from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver  
from rest_framework.authtoken.models import Token  
import django.db.models.deletion

class Usuario(models.Model):
    nombre                  = models.CharField(max_length = 50, on_delete=django.db.models.deletion.SET_NULL)
    USERNAME_FIELD          = models.CharField(max_length = 50, unique=True, on_delete=django.db.models.deletion.SET_NULL)
    rol                     = models.CharField(max_length = 50, on_delete=django.db.models.deletion.SET_NULL)
    identificador           = models.CharField(max_length = 250, on_delete=django.db.models.deletion.SET_NULL)
    foto_perfil             = models.FileField(upload_to="foto_perfil", max_length=100, on_delete=django.db.models.deletion.SET_NULL)
    estaHabilitado          = models.BooleanField(default=True, on_delete=django.db.models.deletion.SET_NULL)
    estado                  = models.CharField(max_length = 250, on_delete=django.db.models.deletion.SET_NULL)
    correo                  = models.CharField(max_length = 50, unique=True, on_delete=django.db.models.deletion.SET_NULL)
    contraseña              = models.CharField(max_length = 250, on_delete=django.db.models.deletion.SET_NULL)
    listaContactos          = models.ManyToManyField("self", blank=True, on_delete=django.db.models.deletion.SET_NULL) 

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
  