from django.shortcuts import render,redirect
from django.contrib import auth
from main.models import Story
from user.models import User
from .models import Recipe
from django.db.models import Q

import detectron2
import cv2,os
import pandas as pd

# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.data.datasets import register_coco_instances

register_coco_instances("meal_detect", {}, "./meal.json", "")
# api로 받아온 식재료 string과 비교 및 레시피 추천

# Create your models here.

class Predictor:
    def __init__(self):
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml"))
        self.cfg.DATASETS.TRAIN = ("meal_detect",)
        self.cfg.DATASETS.TEST = ()
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml")  # Let training initialize from model zoo
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 4
        self.cfg.MODEL.WEIGHTS =  "./recipe/ckpt/model_final.pth"
        self.cfg.merge_from_list(['MODEL.DEVICE','cpu'])
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.55   # set the testing threshold for this model
        self.cfg.DATASETS.TEST = ("meal_detect", )
        self.predictor = DefaultPredictor(self.cfg)
        self.class_map = {
            0 : '단호박',
            1 : '달걀',
            2 : '새우살',
            3 : '브로콜리'
        }

    def infer(self,image_path):
        im = cv2.imread(image_path)
        outputs = self.predictor(im)

        return outputs

    def getItemList(self, image_path):
        out = self.infer(image_path)
        items = list(set(out['instances'].pred_classes.numpy()))

        return [self.class_map[i] for i in items]

def db_recipe(request):
    s= pd.read_csv(r'/Users/seungyounshin/Downloads/기업사회_1석5조_식재료레시피.csv')
    ss = []

    for i in range(len(s)):
        st = (s['질병'][i], s['식재료'][i], s['제목'][i], s['조리법'][i])
        ss.append(st)
    for i in range(len(s)):
        Recipe.objects.create(disease=ss[i][0], ingredient=ss[i][1], title=ss[i][2], recipe=ss[i][3])
    return render(request, 'recipe/match_main.html')

def matching(request,id):
    model = Predictor()
    recipes = Recipe.objects.all()
    storys = list(Story.objects.select_related('writer').filter(writer=id))
    target_story_img_path = './media/'+str([i.image for i in storys][-1]) # story/KakaoTalk_Photo_2021-11-11-17-49-46_kmC0Sl1.jpeg
    itemList = model.getItemList(target_story_img_path) # ['단호박', '새우', '브로콜리']
    print(id, itemList)
    recipe_dict = dict()
    for recipe in list(recipes):
        recipe_dict[str(recipe.title)] = [i.strip() for i in recipe.ingredient.split(',')]
    max_overlap = -1
    max_overlap_recipe_title = None
    for recipe_title in recipe_dict.keys():
        ingds = recipe_dict[recipe_title] # list of str
        overlap = len(list((set(ingds) & set(itemList))))
        if(overlap > max_overlap):
            max_overlap = overlap
            max_overlap_recipe_title = recipe_title

    recipe_matched = Recipe.objects.filter(title=max_overlap_recipe_title)


    return render(request,'recipe/match_main.html', {"recipes":recipe_matched})
    # other = Story.objects.filter(Q(ingredients__exact=key & Recipe.objects.filter(disease=di.disease))

    #if other:

    #else:
    #    return render(request, 'recipe/match_error.html')

def recipe_all(request):
    recipes = Recipe.objects.all()
    return render(request,'recipe/recipe_all.html', {"recipes":recipes})
