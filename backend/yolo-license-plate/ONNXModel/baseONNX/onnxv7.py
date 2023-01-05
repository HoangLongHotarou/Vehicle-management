from ONNXModel.utils.general_v7 import *
from .onnxmodels import BaseYOLO

class YOLOv7(BaseYOLO):
    def __init__(self,w,cuda=False) -> None:
        super().__init__(w, cuda)
    
    def predict(self,img):
        image = img.copy()
        image, ratio, dwdh = letterbox(image, auto=False)
        image = image.transpose((2,0,1))
        image = np.expand_dims(image,0)
        image = np.ascontiguousarray(image)
        im = image.astype(np.float32)
        im /= 255

        outname = [i.name for i in self.session.get_outputs()]
        inname = [i.name for i in self.session.get_inputs()]
        
        inp = {inname[0]:im}
        outputs = self.session.run(outname,inp)[0]
        
        for (_,x0,y0,x1,y1,label,score) in outputs:
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio
            box = box.round().astype(np.int32).tolist()
            yield [*box,score,label]  


class YOLOv7Detect(YOLOv7):
    def __init__(self, cuda=False) -> None:
        w = 'onnx_folder/DetectV7/detect_best.onnx'
        super().__init__(w,cuda)


class YOLOv7Recognize(YOLOv7):
    def __init__(self, cuda=False) -> None:
        # w = 'onnx_folder/RecognizeV7/best.onnx'
        w = 'onnx_folder/RecognizeV7/recognize_best.onnx'
        super().__init__(w,cuda)
