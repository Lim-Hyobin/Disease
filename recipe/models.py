from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    ingredients = models.CharField(max_length= 200)
    recipe = models.TextField()
    disease = models.TextField()

    def __str__(self):
        return self.title