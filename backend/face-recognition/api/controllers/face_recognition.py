from utils.singleton import SingletonMeta
from api.services.crud import InfoCrud
from api.ai_model.face_recognition import FaceRecognition
from core.config import settings
from api.models.face_recognition_info import FaceRecognitionInfo
from utils.string2digit import hash_string2digit
from utils.pyobjectid import PyObjectId

import cloudinary.uploader as cloud_uploader
import time

# from db.database import


class FaceRecognitionController(metaclass=SingletonMeta):
    def __init__(self):
        self.infoCrud = InfoCrud()
        self.faceRecognition = FaceRecognition()

    async def get_face(self, username):
        return await self.infoCrud.get(
            query={'username': username},
            projection={'url': 1, 'embs': 1}
        )

    async def train(self, video_bytes, username, option, info):
        url = None
        id_info = None
        hash_username = hash_string2digit(username)
        if info and option != None:
            url = info.get('url')
            id_info = info.get('_id')
        else:
            result = cloud_uploader.upload(
                video_bytes,
                resource_type="video",
                folder=settings.STORE
            )
            url = result.get('url')
            video_face_obj = FaceRecognitionInfo(
                username=username,
                hash_username=hash_username,
                url=url,
            )
            new_data = await self.infoCrud.add(data=video_face_obj.dict())
            id_info = new_data.get('_id')
        embs = self.faceRecognition.train(url)
        self.faceRecognition.continue_train(embs, hash_username)
        await self.infoCrud.update(
            value=id_info,
            config_data={'len_embs': len(embs)}
        )

    async def remove_face(self, username):
        info = await self.infoCrud.get(
            query={'username': username},
        )
        if info == None:
            return
        url = info.get('url')
        public_id = url.rsplit('/', 1)[1].split('.')[0]
        hash_username = hash_string2digit(username)
        len_embs = info.get('len_embs')
        self.faceRecognition.delete_face(hash_username, len_embs)
        cloud_uploader.destroy(f'{settings.STORE}/{public_id}')
        await self.infoCrud.delete(value=info.get('_id'))

    # async def reload_model(self):
    #     infos,_ = await self.videoFaceCrud.get_all()
    #     names = []
    #     embs =[]
    #     for info in infos:
    #         for emb in info['embs']:
    #             embs.append(emb)
    #             names.append(info['username'])
    #     self.faceRecognition.reload_hnswlib(embs, names)

    async def get_information(self, objs):
        hash_usernames = [obj['hash_username'] for obj in objs]
        usernames, _ = await self.infoCrud.get_all(
            query={
                'hash_username': {
                    '$in': hash_usernames
                }
            },
            projection={
                'username': 1
            }
        )
        result = []
        for i, obj in enumerate(objs):
            obj.pop('hash_username')
            obj['username'] = usernames[i]['username']
            result.append(obj)
        return result

    async def recognition(self, image):
        objs = self.faceRecognition.predict(image)
        result = await self.get_information(objs)
        return result
