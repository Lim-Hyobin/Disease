from django.db import models

class Recipe(models.Model):
    disease = models.CharField(max_length=200)
    ingredient = models.CharField(max_length= 200)
    title = models.CharField(max_length= 200)
    recipe = models.TextField()


    def __str__(self):
        return self.title
