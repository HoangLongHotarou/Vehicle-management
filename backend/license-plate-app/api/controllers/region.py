from api.services.crud import RegionCrud
from api.services.fetchapi import FetchAuthAPI
from utils.singleton import SingletonMeta


class RegionController(metaclass=SingletonMeta):
    def __init__(self):
        self.regionCrud = RegionCrud()

    async def add_region(self,data):
        await self.regionCrud.set_unique(select=[('region',1)])
        return await self.regionCrud.add(data=data)