from django.shortcuts import render,redirect
from django.contrib import auth
from main.models import Story
from user.models import User
from .models import Recipe
from django.db.models import Q

import detectron2
import cv2,os

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
        self.cfg.MODEL.WEIGHTS =  "./ckpt/model_final.pth"
        self.cfg.merge_from_list(['MODEL.DEVICE','cpu'])
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.55   # set the testing threshold for this model
        self.cfg.DATASETS.TEST = ("meal_detect", )
        self.predictor = DefaultPredictor(self.cfg)

    def infer(self,image_path):
        im = cv2.imread(image_path)
        outputs = self.predictor(im)

        return outputs

def matching(request,id):
    recipes = Recipe.objects.all()
    di= User.objects.get(id=id)
    key = str(Recipe.ingredients)

    return render(request,'recipe/match_main.html', {"recipes":recipes})
    # other = Story.objects.filter(Q(ingredients__exact=key & Recipe.objects.filter(disease=di.disease))

    #if other:

    #else:
    #    return render(request, 'recipe/match_error.html')