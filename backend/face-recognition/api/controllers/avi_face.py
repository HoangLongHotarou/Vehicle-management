from utils.singleton import SingletonMeta
from api.services.crud import AviFaceCrud, EmbeddingFaceCrud
from api.ai_model.face_recognition import FaceRecognition
from core.config import settings
import cloudinary.uploader as cloud_uploader
import time

# from db.database import 
class AviFaceController(metaclass=SingletonMeta):
    def __init__(self):
        self.aviFaceCrud = AviFaceCrud()
        self.embeddingFaceCrud = EmbeddingFaceCrud()
        self.faceRecognition = FaceRecognition()
    
    async def add_avi(self,video_bytes,username):
        info = await self.aviFaceCrud.get(query={'username':username},projection={'url':1})
        if info == None:
            result = cloud_uploader.upload(
                video_bytes,
                resource_type="video",
                folder=settings.STORE
            )
            url = result.get('url')
            await self.aviFaceCrud.add(data={'username':username,'url':url})
        else:
            url = info.get('url')
        start = time.time()
        embs = self.faceRecognition.train(url)
        # print(embs)
        await self.embeddingFaceCrud.add(data={'username':username,'embs':embs})
        end = time.time()
        print(f'finish task {end-start}')

    async def recognition(self,image):
        infos,_ = await self.embeddingFaceCrud.get_all()
        names = []
        embs =[]
        for info in infos:
            for emb in info['embs']:
                embs.append(emb)
                names.append(info['username'])
        self.faceRecognition.reload_hnswlib(embs, names)
        result = self.faceRecognition.predict(image)
        return result