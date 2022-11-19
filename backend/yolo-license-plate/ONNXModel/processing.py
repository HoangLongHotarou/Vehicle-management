# from .utils.general import *
from ONNXModel.func.function import *
from ONNXModel.baseONNX.onnxv7 import YOLOv7Detect, YOLOv7Recognize
from ONNXModel.baseONNX.onnxv5 import YOLOv5Detect,YOLOv5Recognize

detect = YOLOv7Detect(cuda=True)
# detect = YOLOv5Detect()
recog = YOLOv5Recognize(cuda=True)
# recog = YOLOv7Recognize(cuda=True)

def processing(image):
    img = image
    result = []
    for (x0,y0,x1,y1) in detection(yolo=detect,image=img):
        plate = {}
        region = img[y0:y1,x0:x1]
        recog_plate = recognize(yolo=recog,image=region)
        if recog_plate == None: continue
        plate['plate'] = recog_plate
        plate['coordinate'] = {'x0':x0,'y0':y0,'x1':x1,'y1':y1}
        result.append(plate)
    return result