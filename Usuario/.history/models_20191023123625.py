from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length = 50)
    usuario = models.CharField(max_length = 50, null = True)
    rol = models.CharField(max_length = 50)
    identificador = models.CharField(max_length = 250)
    foto_perfil = models.FileField(upload_to="foto_perfil", max_length=100)
    estaHabilitado = models.BooleanField(default=True)
    estado = models.CharField(max_length = 250)
    correo = models.CharField(max_length = 50)
    contraseña = models.CharField(max_length = 250)
    listaContactos = models.ManyToManyField("self", blank=True) 

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Usuario(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True