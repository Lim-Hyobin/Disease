from django.urls import path
from .views import *

app_name="deeprunning"

urlpatterns = [
    path("hello/", helloAPI),
] 
