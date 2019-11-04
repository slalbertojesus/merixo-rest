from django.db import models
from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver  
from rest_framework.authtoken.models import Token  
from django.contrib.auth.models import AbstractBaseUser
  
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

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.save(using=self._db)
		return user


class Usuario(AbstractBaseUser):
    nombre                  = models.CharField(max_length = 50)
	username 				= models.CharField(max_length=30, unique=True)
    usuario                 = models.CharField(max_length = 50, unique=True)
    rol                     = models.CharField(max_length = 50)
    identificador           = models.CharField(max_length = 250)
    foto_perfil             = models.FileField(upload_to="foto_perfil", max_length=100)
    estaHabilitado          = models.BooleanField(default=True)
    estado                  = models.CharField(max_length = 250)
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    password                = models.CharField(max_length = 250)
    listaContactos          = models.ManyToManyField("self", blank=True) 


	USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['usuario', 'password', 'nombre', 'correo', 'passwordConfirm', 'rol']

    def __str__(self):
        return self.usuario

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

	objects = UsuarioManager()

	def __str__(self):
		return self.email



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)