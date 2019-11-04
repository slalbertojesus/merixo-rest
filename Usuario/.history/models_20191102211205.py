from django.db import models
from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver  
from rest_framework.authtoken.models import Token  

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
        return self.usuario

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token (sender, instance = None, created = False, **kwargs):
    if created: 
        Token.objects.create(usuario = instance)
  