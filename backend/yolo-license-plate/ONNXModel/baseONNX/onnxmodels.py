from base.singleton import SingletonMeta
import onnxruntime as ort


class BaseYOLO(metaclass=SingletonMeta):
    def __init__(self,w:str, cuda=False) -> None:
        self.providers = ['CUDAExecutionProvider', 'CPUExecutionProvider'] if cuda else ['CPUExecutionProvider']
        self.session = ort.InferenceSession(w,providers=self.providers) 
    
    def predict(self,img):
        pass