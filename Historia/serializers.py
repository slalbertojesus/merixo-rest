from rest_framework import serializers

from django.db import models
import os
from django.conf import settings
from merixorest.utils import is_image_aspect_ratio_valid, is_image_size_valid
from django.core.files.storage import FileSystemStorage

from .models import Story

IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

class StoryId(serializers.ModelSerializer):
	class Meta:
		model = Story
		fields = ['id']

class StoryCommentsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Story
		fields = ['comments']

class StoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Story
		fields = ['title', 'pic', 'date_created','id']

class StoryCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Story
		fields = ['title', 'pic', 'author']

	def save(self):
		try:
			pic = self.validated_data['pic']
			title = self.validated_data['title']
			if len(title) < MIN_TITLE_LENGTH:
				raise serializers.ValidationError({"response":
			 "El titulo debe ser más largo de " + str(MIN_TITLE_LENGTH) + " caracteres."})
			
			story = Story(
								title=title,
								pic=pic,
								author=self.validated_data['author'],
								)

			url = os.path.join(settings.TEMP , str(pic))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in pic.chunks():
					destination.write(chunk)
				destination.close()

			if not is_image_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": 
				"Imagen es muy grande"})

			if not is_image_aspect_ratio_valid(url):
				os.remove(url)
				raise serializers.ValidationError({"response": 
				"Altura de la imagen es inválida"})
			os.remove(url)
			story.save()
			return story

		except KeyError:
			raise serializers.ValidationError({"response": "Debes tener un titulo e imagen"})

