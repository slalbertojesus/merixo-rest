from django.urls import path, include
from rest_framework import routers

from .views import (
	api_detail_usuario_view,
	api_update_usuario_view,
	api_delete_usuario_view,
	api_create_usuario_view,
	api_sing_up_usuario_view,
	api_add_user_view,
)

app_name = 'merixo'

urlpatterns = [
	path('properties', api_detail_usuario_view, name="properties"),
	path('properties/update', api_update_usuario_view, name="update"),
	path('<username>/delete', api_delete_usuario_view, name="delete"),
	path('create', api_create_usuario_view, name="create"),
	path('login',api_sing_up_usuario_view, name="login"),
	path('adduser',api_add_user_view, name="adduser"),
]