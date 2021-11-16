from django.shortcuts import render,redirect
from django.contrib import auth
from main.models import Story
from user.models import User
from .models import Recipe
from django.db.models import Q

# api로 받아온 식재료 string과 비교 및 레시피 추천

# Create your models here.


def matching(request,id):
    recipes = Recipe.objects.all()
    di= User.objects.get(id=id)
    key = str(Recipe.ingredients)
    other = Q(Story.objects.filter(ingredients__exact=key)) & Q(Recipe.objects.filter(disease=di.disease))

    if other:
        return render(request,'recipe/match_main.html', {"recipes":recipes})
    else:
        return render(request, 'recipe/match_error.html')