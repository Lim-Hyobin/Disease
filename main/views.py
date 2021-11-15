from django.shortcuts import render
# Create your views here.

def showmain(request):
    return render(request, 'main/main.html')

from django.shortcuts import get_object_or_404, render,redirect
from .models import Story
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def list(request):
    stories = Story.objects.all()
    return render(request,"main/list.html",{"stories":stories})

def new_story(request):
    return render(request,"main/new_story.html")

def my_story(request):
    stories = Story.objects.filter(writer=request.user)
    return render(request,"main/my_story.html",{"stories":stories})

def create(request):
    new_story=Story()
    new_story.title = request.POST["title"]
    new_story.writer = request.user
    new_story.image = request.FILES.get("image")
    new_story.body = request.POST["body"]
    new_story.ingredients = request.POST["ingredients"]
    new_story.created_at = timezone.now()
    new_story.updated_at = timezone.now()
    new_story.save()
    return redirect("main:detail",new_story.id)


def detail(request,id):
    story = get_object_or_404(Story,pk=id)
    return render(request, "main/detail.html",{"story":story})


def edit_story(request,id):
    story = Story.objects.get(id=id)
    return render(request,"main/edit_story.html",{"story":story})


def update(request, id):
    update_story=Story.objects.get(id=id)
    update_story.title = request.POST["title"]
    update_story.writer = request.user
    update_story.image = request.FILES.get("image")
    update_story.body = request.POST["body"]
    update_story.ingredients = request.POST["ingredients"]
    update_story.updated_at = timezone.now()
    update_story.save()
    return redirect("stories:detail",update_story.id)


def delete(request,id):
    delete_story = Story.objects.get(id=id)
    delete_story.delete()
    return redirect("stories:list")
