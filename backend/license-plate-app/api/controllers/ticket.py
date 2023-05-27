from api.models.ticket import TicketModel, TicketType, VehicleType, RegisterDate
from api.services.crud import TicketCrud
from api.services.fetchapi import FetchAuthAPI
from utils.singleton import SingletonMeta
from utils.pyobjectid import PyObjectId

from datetime import datetime, timedelta
from pytz import timezone


tz = timezone('Asia/Ho_Chi_Minh')

class TicketController(metaclass=SingletonMeta):
    def __init__(self):
        self.tickedCrud = TicketCrud()
    
    async def add_ticket(self, ticket_type, vehicle_type, user_id):
        date = datetime.now(tz)

        ticket =  await self.tickedCrud.get(query={'user_id': PyObjectId(user_id)})

        created_date = date.date()
        
        expire_date = created_date
        
        price = 0
        if vehicle_type == VehicleType.motorcycle:
            price = 2000
        elif vehicle_type == VehicleType.car:
            price = 10000
        if ticket_type == TicketType.month:
            price = price*30
            expire_date += timedelta(days=30)
        elif ticket_type == TicketType.year:
            price = price*30*12
            expire_date += timedelta(days=30*12)
    
        if ticket == None:
            await self.tickedCrud.add(TicketModel(
                user_id=user_id,
                vehicle_type=vehicle_type,
                register_date=[
                    RegisterDate(
                        register_type=ticket_type,
                        created_at=str(created_date),
                        expire_at=str(expire_date),
                        price=price
                    ).dict()
                ]
                ).dict())

# class RegisterDate(BaseModel):
#     register_type: TicketType
#     created_at: str
#     expire_at: str
#     price: str

# class TicketModel(BaseModel):
#     user_id:  PyObjectId
#     vehicle_type: VehicleType
#     register_date: List[RegisterDate]