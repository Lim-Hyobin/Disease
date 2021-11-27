from django.shortcuts import render,redirect
from django.contrib import auth
from main.models import Story
from user.models import User
from .models import Recipe
from django.db.models import Q

# api로 받아온 식재료 string과 비교 및 레시피 추천

# Create your models here.


def matching(request,id):
    recipe_list = Recipe.objects.all()
    return render(request,'recipe/match_main.html', {"recipe_list":recipe_list})
    
    #other = Story.objects.filter(ingredients__exact=key)
    #ingre_key = Story.objects.get(id=id)
    #recipe_list = recipe_list.filter(Q(name__icontains=ingre_key.ingredients)) # 해당 키워드가 name값에 포함되면 출력

    #if other:
       
    #else:
    #    return render(request, 'recipe/match_error.html')