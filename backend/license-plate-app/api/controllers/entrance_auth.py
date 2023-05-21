from api.services.crud import EntranceAuth, EntranceAuthRegion, EntranceAuthUserCrud
from api.services.fetchapi import FetchAuthAPI
from utils.singleton import SingletonMeta
from utils.pyobjectid import PyObjectId


class EntranceAuthController(metaclass=SingletonMeta):
    def __init__(self):
        self.entranceAuthCrud = EntranceAuth()
        self.entranceAuthRegionCrud = EntranceAuthRegion()
        self.entranceAuthUserCrud = EntranceAuthUserCrud()
        self.fetchAuth = FetchAuthAPI()
    
    async def get_all_entrance_auth(self,page,limit):
        return await self.entranceAuthCrud.get_all(
            page=page,
            limit=limit,
            query={'enable':True},
            is_get_info=True
        )
    
    async def create_entrance_auth(self,data):
        new = await self.entranceAuthCrud.add(data)
        return new
    
    async def add_entrance_auth_region(self,data):
        new = await self.entranceAuthRegionCrud.add(data)
        return new
    
    async def delete_entrance_auth_region(self,id):
        await self.entranceAuthRegionCrud.delete(value=id)
    
    async def get_all_entrance_auth_region(self,page,limit):
        return await self.entranceAuthRegionCrud.get_all_entrance_auth_region(page, limit)
    
    async def add_entrance_auth_user(self,data):
        new = await self.entranceAuthUserCrud.add(data)
        return new
    
    async def delete_entrance_auth_user(self,id):
        await self.entranceAuthUserCrud.delete(value=id)
    
    async def get_all_entrance_auth_user(self,page,limit):
        data = await self.entranceAuthUserCrud.get_all_entrance_auth_user(page, limit)
        if data['list'] == []: return data
        ids_users = [str(info['id_user']) for info in data['list']]
        users = await self.fetchAuth.get_user_list(ids_users)
        user_dict = {}
        for user in users:
            user_dict[PyObjectId(user['_id'])] = user
        for i in range(len(data['list'])):
            id_user = data['list'][i].pop('id_user')
            data['list'][i]['user'] = user_dict[id_user]
        return data