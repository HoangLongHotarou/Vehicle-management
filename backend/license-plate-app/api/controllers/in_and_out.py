import asyncio
from datetime import datetime

from api.models.in_and_out import InAndOutModel
from api.models.in_and_out_time import InAndOutTimeModel
from api.services.crud import (InAndOutCrud, InAndOutTimeCrud, RegionCrud,VehicleCrud)
from api.services.fetchapi import FetchAuthAPI, FetchYoloAPI
from pymongo import IndexModel
from pytz import timezone
from utils.singleton import SingletonMeta
from utils.pyobjectid import PyObjectId


tz = timezone('Asia/Ho_Chi_Minh')

class InAndOutController(metaclass=SingletonMeta):
    def __init__(self):
        self.inAndOutCrud = InAndOutCrud()
        self.inAndOutTimeCrud = InAndOutTimeCrud()
        self.vehicleCrud = VehicleCrud()
        self.regionCrud = RegionCrud()
        self.fetchYoloAPI = FetchYoloAPI()
        self.fetchAuth = FetchAuthAPI()
    
    async def predict(self,image):
        return await self.fetchYoloAPI.predict(image)
    
    async def get_aggregate(self,sort,skip,limit,search):
        return await self.inAndOutCrud.filter_detail_in_and_out_time(sort,skip,limit,search)

    async def _preprocessing_data(self,turn,data_list,id_region):
        add_in_and_out = []
        ids_vehicle_has_been_turn = []
        in_and_out_time_ids = []
        ids = []
        for data in data_list:
            in_and_out = data.get('in_and_out')
            if in_and_out == None:
                add_in_and_out.append(
                    {
                        'id_vehicle':PyObjectId(data.get('_id')),
                        'id_region':PyObjectId(id_region)
                    }
                )
            else:
                in_and_out_times = in_and_out['in_and_out_times']
                if in_and_out_times != []:
                    for in_and_out_time in in_and_out_times:
                        if(
                            len(in_and_out_time['times'])>0 and
                            in_and_out_time['times'][-1]['type'] == turn
                        ):
                            ids_vehicle_has_been_turn.append(data['_id'])
                            continue
                        in_and_out_time_ids.append(in_and_out_time['_id'])
                else:
                    ids.append(PyObjectId(in_and_out['_id']))
        return ids,add_in_and_out,in_and_out_time_ids,ids_vehicle_has_been_turn
    
    async def _dotting_in_and_out(
        self,
        date,
        turn,
        ids,
        add_in_and_out,
        in_and_out_time_ids
    ):
        in_and_out_time_objs=[]
        time = {
            'time':str(date.time()),
            'type':turn
        }
        if add_in_and_out != []:
            new_ids = await self.inAndOutCrud.add_in_and_out_list(add_in_and_out)
            ids = [*ids,*new_ids]
        if ids != []:
            for in_and_out_id in ids:
                in_and_out_time_objs.append(
                    {
                        'id_in_and_out':in_and_out_id,
                        'date': str(date.date()),
                        'times':[
                            time
                        ]
                    }
                )
            await self.inAndOutTimeCrud.create_in_and_out_time(in_and_out_time_objs)
        if in_and_out_time_ids != []:
            await self.inAndOutTimeCrud.push_times(in_and_out_time_ids,time)

    async def check_vehicle(self,plates_json,id_region,turn,type_car,task):
        date = datetime.now(tz)
        if plates_json == []: 
            return []
        plates =[plate['plate'] for plate in plates_json] 
        data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle(plates,id_region,str(date.date()))
        users = await self.fetchAuth.get_user_list(ids_user)
        ids_names = {}
        for user in users:
            ids_names[PyObjectId(user['_id'])]=user['username']
        current_plates = [data['plate'] for data in data_list]        
        unknown_plates = []
        for plate in plates:
            if plate not in current_plates:
                object = {
                    'plate': plate,
                    'user_id': None,
                    'type': type_car
                }    
                unknown_plates.append(object)
        new_data_list = []
        if unknown_plates != []:
            new_ids = await self.vehicleCrud.add_many(data=unknown_plates)
            new_ids = [PyObjectId(new_id) for new_id in new_ids]
            new_data_list,_ = await self.vehicleCrud.get_all(query={'_id':{'$in':new_ids}})
        data_list = [*data_list, *new_data_list]
        ids,add_in_and_out,in_and_out_time_ids,ids_vehicle_has_been_turn = await self._preprocessing_data(
            turn=turn,
            data_list=data_list,
            id_region=id_region
        )
        task.add_task(
            self._dotting_in_and_out,
            date,
            turn, 
            ids,
            add_in_and_out,
            in_and_out_time_ids)
        # await self._dotting_in_and_out(date,turn,ids,add_in_and_out,in_and_out_time_ids)
        vehicle_information = []
        for data in data_list:
            info = ''
            if data['_id'] not in ids_vehicle_has_been_turn:
                info = {
                    'date': str(date.date()),
                    'time': str(date.time())
                }
            else:
                info = f"already {turn}"
            object = { 
                'username':ids_names.get(data['user_id'],'unknown'),
                'plate':data['plate'],
                'information': info,
                'turn': turn
            } 
            vehicle_information.append(object)
        return vehicle_information

    async def check_vehicle_realtime(self,plates_json,id_region,turn):
        date = datetime.now(tz)
        if plates_json == []:
            return []
        plates =[plate['plate'] for plate in plates_json] 
        # plates = {}
        # for plate in plates_json:
        #     plates[plate['plate']] = plate['coordinate']
        data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle(plates,id_region,str(date.date()))
        dict_plates = {}
        for plate in plates_json:
            dict_plates[plate['plate']] = plate['coordinate']
        users = await self.fetchAuth.get_user_list(ids_user)
        ids_names = {}
        for user in users:
            ids_names[PyObjectId(user['_id'])]=user['username']
        current_plates = [data['plate'] for data in data_list]       
        unknown_plates = []
        for plate in plates:
            if plate not in current_plates:
                object = {
                    'plate': plate,
                    'coordinate': dict_plates[plate],
                    'information': 'vehicle not yet register'
                }
                unknown_plates.append(object) 
        ids,add_in_and_out,in_and_out_time_ids,ids_vehicle_has_been_turn = await self._preprocessing_data(
            turn=turn,
            data_list=data_list,
            id_region=id_region
        )
        
        await self._dotting_in_and_out(date,turn,ids,add_in_and_out,in_and_out_time_ids)
        vehicle_information = []
        for data in data_list:
            info = ''
            if data['_id'] not in ids_vehicle_has_been_turn:
                info = {
                    'date': str(date.date()),
                    'time': str(date.time())
                }
            else:
                info = f"already {turn}"
            object = { 
                'username':ids_names.get(data['user_id'],'unknown'),
                'plate':data['plate'],
                'coordinate': dict_plates[data['plate']],
                'information': info,
            } 
            vehicle_information.append(object)
        return {"register":vehicle_information,"not_registered":unknown_plates,"turn":turn}
    
    def calculate_reduce_date(self,date_split):
        date_split[2] -= 1
        if date_split[2] == 0:
            date_split[1] -= 1
            if date_split[1] == 0:
                date_split[1] = 12
                date_split[0] -= 1
                if date_split[0] == -1:
                    date_split = [0,1,1]
                    return date_split
            if (1<=date_split[1]<=7 and date_split[1]%2!=0) or (8<=date_split[1]<=12 and date_split[1]%2==0):
                date_split[2] = 31
            elif date_split[1] == 2:
                if date_split[0] % 4 == 0:
                    date_split[2] = 29
                else:
                    date_split[2] = 28
            else:
                date_split[2] = 30
        return date_split
    
    def convert_int_date(self,date):
        return [int(date) for date in date.split('-')]
    
    def convert_str_date(self,date):
        return f'{date[0]:04}-{date[1]:02}-{date[2]:02}'
    
    def convert_day_month(self,date):
        return f'{date[2]:02}/{date[1]:02}'
    
    async def statistic_in_and_out(self,date):
        date_split = self.convert_int_date(date)
        data = []
        for _ in range(6,-1,-1):
            date_split = self.calculate_reduce_date(date_split)
            str_date = self.convert_str_date(date_split)
            statistic = await self.inAndOutTimeCrud.show_total_in_and_out_time(str_date)
            statistic['date'] = self.convert_day_month(date_split)
            data.append(statistic)
        return data

    # async def _preprocessing_data(self,turn,data_list,id_region):
    #     add_in_and_out = []
    #     ids_vehicle_has_been_turn = []
    #     # in_and_out_time_ids = []
    #     ids_in_out = {}
    #     vehicle_in_out = {}
    #     vehicles = set()
    #     add_in_out_vehicle = set()
    #     for data in data_list:
    #         vehicles.add(data.get('_id'))
    #         in_and_out = data.get('in_and_out')
    #         if data['_id'] in ids_vehicle_has_been_turn: continue
    #         if in_and_out == None:
    #             add_in_out_vehicle.add(data.get('_id'))
    #         elif id_region != in_and_out.get('id_region'):
    #             in_and_out_time = in_and_out.get('in_and_out_time')
    #             if in_and_out_time == None:
    #                 continue
    #             elif(
    #                 len(in_and_out_time['times'])>0 and
    #                 in_and_out_time['times'][-1]['type'] == turn
    #             ):
    #                 ids_vehicle_has_been_turn.append(data['_id'])
    #                 vehicle_in_out.pop(data['_id'])
    #         elif id_region == in_and_out.get('id_region'):
    #             in_and_out_time = in_and_out.get('in_and_out_time')
    #             if in_and_out_time == None:
    #                 ids_in_out[data.get('_id')] = PyObjectId(in_and_out['_id'])
    #             elif(
    #                 len(in_and_out_time['times'])>0 and
    #                 in_and_out_time['times'][-1]['type'] == turn
    #             ):
    #                 ids_vehicle_has_been_turn.append(data['_id'])
    #                 vehicle_in_out.pop(data['_id'])
    #             else:
    #                 vehicle_in_out[data['_id']]=in_and_out_time['_id']
    #     # if count == 0:
    #     for vehicle in vehicles:
    #         if vehicle not in vehicle_in_out.keys() or vehicle not in add_in_out_vehicle or vehicle not in ids_in_out.key():
    #             if vehicle in ids_vehicle_has_been_turn: continue
    #             add_in_out_vehicle.add(vehicle)
    #     for vehicle in add_in_out_vehicle:
    #         add_in_and_out.append(
    #             {
    #                 'id_vehicle':PyObjectId(vehicle),
    #                 'id_region':PyObjectId(id_region)
    #             }
    #         )
    #     in_and_out_time_ids = list(vehicle_in_out.values())
    #     ids = list(ids_in_out.values())
    #     return ids, add_in_and_out, in_and_out_time_ids,ids_vehicle_has_been_turn

    # async def check_vehicle(self,plates_json,id_region,turn,type_car,task):
    #     date = datetime.now(tz)
    #     if plates_json == []: 
    #         return []
    #     plates =[plate['plate'] for plate in plates_json] 
    #     data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle(plates,str(date.date()))
    #     print(data_list)
    #     users = await self.fetchAuth.get_user_list(ids_user)
    #     ids_names = {}
    #     for user in users:
    #         ids_names[PyObjectId(user['_id'])]=user['username']
    #     current_plates = [data['plate'] for data in data_list]        
    #     unknown_plates = []
        
    #     for plate in plates:
    #         if plate not in current_plates:
    #             object = {
    #                 'plate': plate,
    #                 'user_id': None,
    #                 'type': type_car
    #             }
    #             unknown_plates.append(object)
        
    #     new_data_list = []
    #     if unknown_plates != []:
    #         new_ids = await self.vehicleCrud.add_many(data=unknown_plates)
    #         new_ids = [PyObjectId(new_id) for new_id in new_ids]
    #         new_data_list,_ = await self.vehicleCrud.get_all(query={'_id':{'$in':new_ids}})
    #     data_list = [*data_list, *new_data_list]
        
        
    #     ids,add_in_and_out,in_and_out_time_ids,ids_vehicle_has_been_turn = await self._preprocessing_data(
    #         turn=turn,
    #         data_list=data_list,
    #         id_region=id_region
    #     )
        
    #     print(ids)
    #     print(add_in_and_out)
    #     print(in_and_out_time_ids)
    #     print(ids_vehicle_has_been_turn)
        
    #     # task.add_task(
    #     #     self._dotting_in_and_out,
    #     #     date,
    #     #     turn, 
    #     #     ids,
    #     #     add_in_and_out,
    #     #     in_and_out_time_ids)
    #     # # await self._dotting_in_and_out(date,turn,ids,add_in_and_out,in_and_out_time_ids)
    #     # vehicle_information = []
    #     # for data in data_list:
    #     #     info = ''
    #     #     if data['_id'] not in ids_vehicle_has_been_turn:
    #     #         info = {
    #     #             'date': str(date.date()),
    #     #             'time': str(date.time())
    #     #         }
    #     #     else:
    #     #         info = f"already {turn}"
    #     #     object = { 
    #     #         'username':ids_names.get(data['user_id'],'unknown'),
    #     #         'plate':data['plate'],
    #     #         'information': info,
    #     #         'turn': turn
    #     #     } 
    #     #     vehicle_information.append(object)
    #     # return vehicle_information
    

    # async def dotting_in_and_out(self,date,turn,data_list,id_region):
    #     add_in_and_out = []
    #     in_and_out_time_objs = []
    #     in_and_out_time_ids = []
    #     ids = []
    #     time = {
    #         'time':str(date.time()),
    #         'type':turn.value
    #     }
    #     for data in data_list:
    #         in_and_out = data.get('in_and_out')
    #         if in_and_out == None:
    #             add_in_and_out.append(
    #                 {
    #                     'id_vehicle':PyObjectId(data.get('_id')),
    #                     'id_region':PyObjectId(id_region)
    #                 }
    #             )
    #         else:
    #             in_and_out_times = in_and_out['in_and_out_times']
    #             if in_and_out_times != []:
    #                 print(in_and_out_times)
    #                 for in_and_out_time in in_and_out_times:
    #                     if len(in_and_out_time['times'])>0 and in_and_out_time['times'][-1]['type'] == turn.value:
    #                         continue
    #                     in_and_out_time_ids.append(data['_id'])
    #             else:
    #                 ids.append(PyObjectId(in_and_out['_id']))
    #     if add_in_and_out != []:
    #         new_ids = await self.inAndOutCrud.add_in_and_out_list(add_in_and_out)
    #         ids = [*ids,*new_ids]
    #     if ids != []:
    #         for in_and_out_id in ids:
    #             in_and_out_time_objs.append(
    #                 {
    #                     'id_in_and_out':in_and_out_id,
    #                     'date': str(date.date()),
    #                     'times':[
    #                         time
    #                     ]
    #                 }
    #             )
    #         await self.inAndOutTimeCrud.create_in_and_out_time(in_and_out_time_objs)
    #     if in_and_out_time_ids != []:
    #         await self.inAndOutTimeCrud.push_times(in_and_out_time_ids,time)

    # async def check_vehicle(self,image,id_region,turn,task):
    #     date = datetime.now(tz)
    #     print(str(date.date()))
    #     plates_json = await self.predict(image)
    #     plates =[plate['plate'] for plate in plates_json] 
    #     data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle(plates,id_region,str(date.date()))

    #     users = await self.fetchAuth.get_user_list(ids_user)

    #     task.add_task(self.dotting_in_and_out,date, turn, data_list,id_region)

    #     vehicle_information = []
    #     plates_exits = []
    #     for i in range(len(data_list)):
    #         object = {
    #             'username': users[i].get('username'),
    #             'plate':data_list[i].get('plate'),
    #             'date':str(date.date()),
    #             'time':str(date.time()),
    #             'detail':f"valid to turn {turn.value}"
    #         }
    #         plates_exits.append(data_list[i].get('plate'))
    #         vehicle_information.append(object)
    #     for plate in plates:
    #         if plate not in plates_exits:
    #             object = {
    #                 'username': 'unknown',
    #                 'plate':plate,
    #                 'date':str(date.date()),
    #                 'time':str(date.time()),
    #                 'detail':f"not valid to turn {turn.value}"
    #             }
    #             vehicle_information.append(object)
    #     return vehicle_information
