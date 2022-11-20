import cv2
import torch
from yolo_function.baseYOLO.detect import BaseDetect
from yolo_function.baseYOLO.recognize import BaseRecognize
from yolo_function.baseProcessing.processing import BaseProcessing


class YoloV5Detect(BaseDetect):
    def __init__(self):
        super().__init__('ultralytics/yolov5', 'pt_folder/yolov5_detect/best')

class YoloV5Recognize(BaseRecognize):
    def __init__(self):
        super().__init__('ultralytics/yolov5', 'pt_folder/yolov5_recog/best')

class YOLOV5Processing(BaseProcessing):
    def __init__(self):
        detect = YoloV5Detect()
        recog = YoloV5Recognize()
        super().__init__(detect,recog)