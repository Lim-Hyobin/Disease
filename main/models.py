from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User 이거 못쓰던데 물어보기

User = settings.AUTH_USER_MODEL
# Create your models here.

class Story(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="story/",null=True, blank=True)
    ingredients = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=False)
    updated_at = models.DateTimeField(auto_now=True)
