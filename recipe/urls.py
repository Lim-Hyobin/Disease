from django.urls import path
from .views import *

app_name="recipe"

urlpatterns = [
    path("matching/<int:id>",matching, name="matching" ),
    path("db_recipe/",db_recipe, name="db_recipe"),
    path("recipe_all/",recipe_all, name="recipe_all"),
]
