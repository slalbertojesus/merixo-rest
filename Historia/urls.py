from django.urls import path, include
from rest_framework import routers

from .views import (
	api_create_story_view,
	api_delete_story_view,
	api_get_all_stories_view,
	api_add_story_favorites_view,
	api_get_fav_stories_view,
	api_delete_from_favorites_view,
	api_get_feed_view,
	api_get_story_comments_view,
	api_add_like_view,
	api_add_comment_view,
)

app_name = 'Historia'

urlpatterns = [
	path('createstory', api_create_story_view, name="createstory"),
	path('<slug>/delete', api_delete_story_view, name="delete"),
	path('getallstories', api_get_all_stories_view, name="getallstories"),
	path('addtofavorites', api_add_story_favorites_view, name="addtofavorites"),
	path('getfavstories', api_get_fav_stories_view, name="getfavstories"),
	path('deletefromfavorites', api_delete_from_favorites_view, name="deletefromfavorites"),
	path('getfeed', api_get_feed_view, name="getfeed"),
	path('getcomments', api_get_story_comments_view, name="getcomments"),
	path('addcomment', api_add_comment_view, name="addcomment"),
	path('addlike', api_add_like_view, name="addlike"),
]