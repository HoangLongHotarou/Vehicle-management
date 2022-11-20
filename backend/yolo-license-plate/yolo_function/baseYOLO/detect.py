import torch
from yolo_function.baseYOLO.yolo import BaseLicensePlateYOLO

class BaseDetect(BaseLicensePlateYOLO):
    def __init__(self, yolo_version, pt_file):
        super().__init__(yolo_version, pt_file)
    
    def detect(self,img):
        detect = self.model(img)
        return detect.xyxy[0]