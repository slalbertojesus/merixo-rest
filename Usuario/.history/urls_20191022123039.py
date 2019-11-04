from django.urls import path, include
from .models import views 
from rest_framework import routers

from .views import(
	detalles_usuario_view,
	api_update_blog_view,
	api_delete_blog_view,
	api_create_blog_view,
)

app_name = 'blog'

urlpatterns = [
	path('<identificador>/', detalles_usuario_view, name="detail"),
]