from django.contrib import admin
from .models import Story
from .models import Like

admin.site.register(Story)
admin.site.register(Like)
