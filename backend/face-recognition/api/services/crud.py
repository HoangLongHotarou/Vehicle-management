from base.crud import BaseCrud
from pymongo import IndexModel

app='face_recognition'

class InfoCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_info')

    async def add(self, data: dict, session=None):
        # await self.set_unique([('username', 1)])
        index1 = IndexModel([('username',1)],unique=True)
        index2 = IndexModel([('hash_username',1)],unique=True)
        await self.set_multi_key([index1, index2])
        return await super().add(data=data, session=session)
