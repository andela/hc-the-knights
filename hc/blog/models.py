from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from datetime import datetime

# Create your models here.
class BlogCategory(models.Model):
    title = models.CharField(max_length=300, unique = True)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.title

class Blog(models.Model):
    author = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(max_length=300, blank = False)
    content = models.TextField(blank = False)
    slug = models.SlugField(unique = True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE) #one to many
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    draft = models.BooleanField(default = False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    # publish = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

def create_slug(instance, modelObject, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = modelObject.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, modelObject, new_slug=new_slug)
    return slug

'''
unique_slug_generator
'''
from .utils import unique_slug_generator

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

class Comment(models.Model):
    post = models.ForeignKey(Blog, related_name='comments')
    name = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)





pre_save.connect(pre_save_post_receiver, sender=Blog)
pre_save.connect(pre_save_post_receiver, sender=BlogCategory)