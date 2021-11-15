from django.urls import path
from .views import *

app_name="recipe"

urlpatterns = [
    path("matching/<int:id>",matching, name="matching" ),

] 