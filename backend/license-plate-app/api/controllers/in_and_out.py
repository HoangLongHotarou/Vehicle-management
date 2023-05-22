import asyncio
from datetime import datetime

from api.models.in_and_out import InAndOutModel
from api.models.in_and_out_time import InAndOutTimeModel
from api.models.check_exist_face import CheckExistFace
from api.services.crud import (InAndOutCrud, InAndOutTimeCrud, RegionCrud,VehicleCrud, 
                            CheckExistFaceCrud, EntranceAuthUserCrud)
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
        self.checkExistFaceCrud = CheckExistFaceCrud()
        self.entranceAuthUserCrud = EntranceAuthUserCrud()
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
    
    async def _preprocessing_data_v2(self,turn,data_list,id_region,date):
        add_in_and_out = []
        vehicle_has_been_turn = {}
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
                in_and_out_time = in_and_out.get('in_and_out_time',None)
                if in_and_out_time != None:
                    if(
                        len(in_and_out_time['times'])>0 and
                        in_and_out_time['times'][-1]['type'] == turn
                    ):
                        vehicle_has_been_turn[data['_id']] = {
                                'date':in_and_out_time['date'],
                                'time': in_and_out_time['times'][-1]['time']
                            }
                        continue
                    if in_and_out_time['date'] == date:
                        in_and_out_time_ids.append(in_and_out_time['_id'])
                    else:
                        ids.append(PyObjectId(in_and_out['_id']))
                else:
                    ids.append(PyObjectId(in_and_out['_id']))
        return ids,add_in_and_out,in_and_out_time_ids,vehicle_has_been_turn
    
    async def _mark_in_and_out_for_one_user(self,turn,data,id_region,date):
        time = {
            'time':str(date.time()),
            'type':turn
        }
        
        add_in_and_out = None
        in_and_out_time_id = None
        in_and_out_id = None
        vehicle_has_been_turn = None
        
        in_and_out = data.get('in_and_out')
        
        if in_and_out == None:
            add_in_and_out = {
                    'id_vehicle':PyObjectId(data.get('_id')),
                    'id_region':PyObjectId(id_region)
            }
            in_and_out = await self.inAndOutCrud.add(data=add_in_and_out)
        in_and_out_time = in_and_out.get('in_and_out_time',None)
        if in_and_out_time:
            if(
                len(in_and_out_time['times'])>0 and
                in_and_out_time['times'][-1]['type'] == turn
            ):
                vehicle_has_been_turn = {
                        'date':in_and_out_time['date'],
                        'time': in_and_out_time['times'][-1]['time']
                    }
                return False, vehicle_has_been_turn
            elif in_and_out_time['date'] == date:
                in_and_out_time_id = in_and_out_time['_id']
                await self.inAndOutTimeCrud.push_times_one_user(in_and_out_time_id,time)
            else:
                in_and_out_id = PyObjectId(in_and_out['_id'])
        else:
            in_and_out_id = PyObjectId(in_and_out['_id'])
        if in_and_out_id:
            in_and_out_time_obj = {
                'id_in_and_out':in_and_out_id,
                'date': str(date.date()),
                'times':[
                    time
                ]
            }
            await self.inAndOutTimeCrud.add(in_and_out_time_obj)
        return True, None
    
    
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

    async def check_vehicle_v2(self,plates_json,id_region,turn):
        date = datetime.now(tz)
        if plates_json == []: 
            return []
        plates =[plate['plate'] for plate in plates_json] 
        data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle_v2(plates,id_region,str(date.date()))
        # data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle(plates,id_region,str(date.date()))
        
        print(data_list)
        return "ehehe"
    
    async def check_vehicle_v3(self,id_region):
        date = datetime.now(tz)
        # if plates_json == []: 
            # return []
        # plates =[plate['plate'] for plate in plates_json]
        plates = ['49E1-22222','59M1-81859','54Y8-8280'] 
        data_list = await self.vehicleCrud.filter_role_access(plates,id_region)
        return "ehehe"

    async def check_vehicle_realtime(self,plate_json,id_region,turn):
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
    
    async def check_vehicle_realtime_v2(self,plates_json,id_region,turn):
        vehicle_information = []
        role_plates = {}
        unknown_plates = []

        date = datetime.now(tz)
        if plates_json == []:
            return []
        plates = [plate['plate'] for plate in plates_json] 
        
        dict_plates = {}
        for plate in plates_json:
            dict_plates[plate['plate']] = plate['coordinate']
        
        # filter all role of user
        info_plate = await self.vehicleCrud.filter_role_access(plates, id_region)
        
        for dict in info_plate:
            if dict['plate'] not in role_plates:
                role_plates[dict['plate']] = [dict['entrance_auth_user']['entrance_auth']['name']]
            else:
                role_plates[dict['plate']].append(dict['entrance_auth_user']['entrance_auth']['name'])
        
        # print(role_plates.keys()==[])
        
        for plate in plates:
            if plate not in list(role_plates.keys()):
                object = {
                    'plate': plate,
                    'coordinate': dict_plates[plate],
                    'information': 'vehicle not yet register'
                }
                unknown_plates.append(object) 
        
        if role_plates != {}:
            # filter vehicle is accessed in today
            data_list,ids_user = await self.vehicleCrud.filter_detail_vehicle_v2(list(role_plates.keys()),id_region,str(date.date()))
            
            # Get user list
            users = await self.fetchAuth.get_user_list(ids_user)
            ids_names = {}
            for user in users:
                ids_names[PyObjectId(user['_id'])]=user['username']
            current_plates = [data['plate'] for data in data_list]       
            
            # preprocessing data
            ids,add_in_and_out,in_and_out_time_ids, vehicle_has_been_turn = await self._preprocessing_data_v2(
                turn=turn,
                data_list=data_list,
                id_region=id_region,
                date = str(date.date())
            )
            
            await self._dotting_in_and_out(date,turn,ids,add_in_and_out,in_and_out_time_ids)
            for data in data_list:
                info = ''
                if data['_id'] not in vehicle_has_been_turn.keys():
                    info = {
                        'message': f'turn {turn}',
                        'date': str(date.date()),
                        'time': str(date.time())
                    }
                else:
                    info = {
                        'message': f"already {turn}",
                        'date': vehicle_has_been_turn[data['_id']]['date'],
                        'time': vehicle_has_been_turn[data['_id']]['time']
                    }
                object = { 
                    'username':ids_names.get(data['user_id'],'unknown'),
                    'plate':data['plate'],
                    'role': role_plates[data['plate']],
                    'coordinate': dict_plates[data['plate']],
                    'information': info,
                } 
                vehicle_information.append(object)
        return {"register":vehicle_information,"not_registered":unknown_plates,"turn":turn}
    
    def return_data(self, register, not_register, warning, turn):
        return {"register": register,"not_registered": not_register,"warning": warning,"turn": turn}
    
    async def check_vehicle_realtime_for_one_user(self,plates_json,id_region,turn):
        vehicle_information = []
        role_plates = {}
        # unknown_plates = []
        register = []
        not_register = []
        warning = []

        date = datetime.now(tz)
        if plates_json == []:
            return []
        plate = plates_json[0]['plate']
        coordinate = plates_json[0]['coordinate']

        data = await self.vehicleCrud.filter_role_access_for_one_user(plate, id_region)
        if not data:
            not_register.append(
                {
                    'plate': plate,
                    'information': 'vehicle not yet registered',
                    'coordinate':coordinate
                }
            )
            return self.return_data(register, not_register, warning, turn)
        
        user = await self.fetchAuth.get_user(data['user_id'])
        username = user['username']
        
        check = await self.is_exist_face(username, id_region)
        
        if not check:
            warning.append(
                {
                    'plate': plate,
                    'type': data['type'],
                    'owner': username,
                    'information': "Unauthorized driver detected",
                    'coordinate':coordinate
                }
            )
            test = self.return_data(register, not_register, warning, turn)
            print(test)
            return test
        
        role = await self.entranceAuthUserCrud.get_role_for_user(id_user=data['user_id'])
        
        if not data['entrance_auth_user']:
            warning.append({
                'plate': plate,
                'type': data['type'],
                'username': username,
                'role': role,
                'information': "Warning! Unauthorized vehicle approaching"
            })
            return self.return_data(register, not_register, warning, turn)

        data_vehicle = await self.vehicleCrud.filter_detail_vehicle_v2_for_one_user(plate,id_region,str(date.date()))

        check, vehicle_has_been_turn = await self._mark_in_and_out_for_one_user(turn, data_vehicle, id_region, date)
        
        if not vehicle_has_been_turn:
            info = {
                'message': f'turn {turn}',
                'date': str(date.date()),
                'time': str(date.time())
            }
        else:
            info = {
                'message': f"already {turn}",
                'date': vehicle_has_been_turn['date'],
                'time': vehicle_has_been_turn['time']
            }
        register.append(
            { 
                'username':username,
                'plate':data['plate'],
                'role': role,
                'coordinate': dict_plates[data['plate']],
                'information': info,
            } 
        )
        return self.return_data(register, not_register, warning, turn)
    
    async def add_username_to_exist_face(self,username, id_region):
        data = await self.checkExistFaceCrud.get(query={'username':username,'id_region':PyObjectId(id_region)})
        print(data)
        if data == None:
            data = await self.checkExistFaceCrud.add(
                CheckExistFace(username=username,id_region=id_region, created_at= datetime.utcnow()).dict()
            )
        return data
    
    async def is_exist_face(self,username, id_region):
        data = await self.checkExistFaceCrud.get(query={'username':username, 'id_region': PyObjectId(id_region)})
        return True if data else False
    
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