from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver  
from rest_framework.authtoken.models import Token  
  
class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre, email, usuario, password, rol):
        user = self.create_user(
            email=self.normalize_email(email),
            nombre = nombre,
            password=password,
            username=usuario,
            rol = rol,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    nombre                  = models.CharField(max_length = 50)
    usuario                 = models.CharField(max_length = 50, unique=True)
    rol                     = models.CharField(max_length = 50)
    foto_perfil             = models.FileField(upload_to="foto_perfil", max_length=100)
    estaHabilitado          = models.BooleanField(default=True)
    estado                  = models.CharField(max_length = 250)
    email 					= models.CharField(max_length=60, unique=True)
    password                = models.CharField(max_length = 250)
    listaContactos          = models.ManyToManyField("self", blank=True) 
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usuario', 'password', 'nombre', 'rol']

    objects = UsuarioManager()

    def __str__(self):
        return self.usuario

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)