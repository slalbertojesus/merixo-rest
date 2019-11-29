from django.urls import path, include
from rest_framework import routers

from .views import (
	api_create_story_view,
)

app_name = 'Historia'

urlpatterns = [
	path('createstory', api_create_story_view, name="createstory"),
]