from ONNXModel.utils.general_v5 import *
from .onnxmodels import BaseYOLO

class YOLOv5(BaseYOLO):
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
        outputs = torch.from_numpy(outputs).to(torch.device('cpu'))
        outputs = non_max_suppression(outputs)[0]
        
        for (x0,y0,x1,y1,score,label) in outputs:
            box = np.array([x0,y0,x1,y1])
            box -= np.array(dwdh*2)
            box /= ratio[0]
            box = box.round().astype(np.int32).tolist()
            yield [*box,score,label]


class YOLOv5Detect(YOLOv5):
    def __init__(self, cuda=False) -> None:
        w = 'onnx_folder/DetectV5/best.onnx'
        super().__init__(w,cuda)


class YOLOv5Recognize(YOLOv5):
    def __init__(self, cuda=False) -> None:
        w = 'onnx_folder/RecognizeV5/best.onnx'
        super().__init__(w,cuda)
