from django.db import models

# Create your models here.
class SwiperContent(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=30)
    answer = models.IntegerField()