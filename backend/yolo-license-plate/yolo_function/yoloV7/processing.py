import cv2
import torch
from yolo_function.baseYOLO.detect import BaseDetect
from yolo_function.baseYOLO.recognize import BaseRecognize
from yolo_function.baseProcessing.processing import BaseProcessing


class YoloV7Detect(BaseDetect):
    def __init__(self):
        super().__init__('WongKinYiu/yolov7', 'pt_folder/yolov7_tiny/detect_best.pt')

class YoloV7Recognize(BaseRecognize):
    def __init__(self):
        super().__init__('WongKinYiu/yolov7', 'pt_folder/yolov7_tiny/recognize_best.pt')

class YOLOV7Processing(BaseProcessing):
    def __init__(self):
        detect = YoloV7Detect()
        recognize = YoloV7Recognize()
        super().__init__(detect, recognize)