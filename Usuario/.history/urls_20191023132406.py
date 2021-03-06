from django.urls import path, include
from rest_framework import routers

from .views import (
	api_detail_usuario_view,
	api_update_usuario_view,
	api_delete_usuario_view,
	api_create_usuario_view,
)

app_name = 'merixo'

urlpatterns = [
	path('<identificador>/', api_detail_usuario_view, name="detail"),
	path('<identificador>/update', api_update_usuario_view, name="update"),
	path('<identificador>/delete', api_delete_usuario_view, name="delete"),
	path('create', api_create_usuario_view, name="create"),
]