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
        self.class_map = {
            0 : '단호박',
            1 : '달걀',
            2 : '새우',
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

if __name__=="__main__":
    modelWrapper = Predictor()
    out = modelWrapper.getItemList(
        "/Users/seungyounshin/Desktop/DGU/4-1/기사프/data/images/KakaoTalk_Photo_2021-11-11-17-49-46.jpeg")
    print(out)
