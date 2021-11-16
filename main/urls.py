from django.urls import path
from .views import *

app_name="main"

urlpatterns = [
    path('list/',list,name="list"),
    path('new_story/',new_story,name="new_story"),
    path('create/',create,name="create"),
    path('detail<int:id>',detail,name="detail"),
    path('edit_story/<int:id>',edit_story,name="edit_story"),
    path('update/<int:id>',update,name="update"),
    path('delete/<int:id>',delete,name="delete"),
] 