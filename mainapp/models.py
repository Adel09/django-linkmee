from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Page(models.Model):
    name = models.CharField(max_length=45)
    bio = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/', null=True)
    views = models.IntegerField(default=0, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='page')
    def __str__(self):
        return self.name

class Link(models.Model):
    title = models.CharField(max_length=45)
    url = models.CharField(max_length=75)
    count = models.IntegerField(default=0)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='links')
    def __str__(self):
        return self.title
