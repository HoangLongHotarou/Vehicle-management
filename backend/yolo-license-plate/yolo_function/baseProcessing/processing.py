import concurrent.futures

from base.singleton import SingletonMeta
from yolo_function.baseYOLO.detect import BaseDetect
from yolo_function.baseYOLO.recognize import BaseRecognize


class BaseProcessing(metaclass=SingletonMeta):
    def __init__(self, detect, recognize):
        self.detector: BaseDetect = detect
        self.recognition: BaseRecognize = recognize
    
    def predict(self,frame):
        result = []
        regions = self.detector.detect(frame)
        for (x0,y0,x1,y1,score,label) in regions:
            if float(score) < 0.75: continue
            plate = {}
            LpRegion = frame[int(y0):int(y1),int(x0):int(x1)]
            recog_plate = self.recognition.predict(LpRegion)
            if recog_plate == None: continue
            plate['plate'] = recog_plate
            plate['coordinate'] = {'x0':int(x0),'y0':int(y0),'x1':int(x1),'y1':int(y1)}
            result.append(plate)
        return result