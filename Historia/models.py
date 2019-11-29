from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

def upload_location(instance, filename, **kwargs):
	file_path = 'stories/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author.username), title=str(instance.title), filename=filename
		)
	return file_path

class Story(models.Model):
    pic 				= models.ImageField(upload_to=upload_location, null=False, blank=False)
    likes        		= models.IntegerField(default = 0, blank=False)
    dislikes     		= models.IntegerField(default = 0, blank=False)
    date_created	    = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    is_activated 		= models.BooleanField(default = True)
    title       		= models.CharField(max_length=30)
    author 				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug 				= models.SlugField(blank=True, unique=True)

@receiver(post_delete, sender=Story)
def submission_delete(sender, instance, **kwargs):
	instance.pic.delete(False)

def pre_save_story_receiever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_story_receiever, sender=Story)
