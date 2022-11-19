from api.models.vehicle import VehicleModel
from api.services.crud import VehicleCrud
from api.services.fetchapi import FetchAuthAPI
from utils.singleton import SingletonMeta


class VehicleController(metaclass=SingletonMeta):
    def __init__(self):
        self.vehicleCrud  = VehicleCrud()
        self.fetchAPI = FetchAuthAPI()
    
    async def insert_json(self,data:list):
        await self.vehicleCrud.add_many(data)
    
    async def add_vehicle_for_current_user(self,object,id_user):
        await self.vehicleCrud.set_unique([('plate', 1)])
        vehicle = VehicleModel(**{**object.dict(),'user_id':id_user})
        return await self.vehicleCrud.add(data=vehicle.dict())
