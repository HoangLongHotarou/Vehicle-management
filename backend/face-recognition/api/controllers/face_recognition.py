from utils.singleton import SingletonMeta
from api.services.crud import EmbeddingFaceCrud
from api.ai_model.face_recognition import FaceRecognition
from core.config import settings
from api.models.embedding_face import EmbeddingFace
import cloudinary.uploader as cloud_uploader
import time

# from db.database import 
class FaceRecognitionController(metaclass=SingletonMeta):
    def __init__(self):
        self.embeddingFaceCrud = EmbeddingFaceCrud()
        self.faceRecognition = FaceRecognition()
    
    async def get_face(self, username):
        return await self.embeddingFaceCrud.get(query={'username':username},projection={'url':1,'embs':1})
    
    async def train(self,video_bytes,username):
        start = time.time()
        result = cloud_uploader.upload(
            video_bytes,
            resource_type="video",
            folder=settings.STORE
        )
        url = result.get('url')
        embs = self.faceRecognition.train(url)
        embedding_face_obs = EmbeddingFace(
            username=username,
            url=url,
            embs=embs
        )
        await self.embeddingFaceCrud.add(data=embedding_face_obs.dict())
        await self.reload_model()
        end = time.time()
        print(f'finish task {end-start}')

    async def reload_model(self):
        infos,_ = await self.embeddingFaceCrud.get_all()
        names = []
        embs =[]
        for info in infos:
            for emb in info['embs']:
                embs.append(emb)
                names.append(info['username'])
        self.faceRecognition.reload_hnswlib(embs, names)

    async def recognition(self,image):
        result = self.faceRecognition.predict(image)
        return result