from datetime import datetime

from api.models.in_and_out import InAndOutModel
from api.models.in_and_out_time import InAndOutTimeModel, Time
from base.crud import BaseCrud
from pymongo import IndexModel
from pytz import timezone
from utils.pyobjectid import PyObjectId
from pymongo import IndexModel
import math

app = 'license_plate'
tz = timezone('Asia/Ho_Chi_Minh')

class VehicleCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_vehicle')
    
    async def filter_detail_vehicle(self,plates,id_region,date):
        pipeline=[
            {
                '$match':{
                    'plate':{
                        "$in":plates
                    }
                }
            },
            {
                '$lookup':{
                    'from':'license_plate_in_and_out',
                    'localField':'_id',
                    'foreignField':'id_vehicle',
                    'as':'in_and_out',
                    'pipeline':[
                        {
                            '$match':{
                                'id_region':id_region
                            }
                        },
                        {
                            '$lookup':{
                                'from':'license_plate_region',
                                'localField': 'id_region',
                                'foreignField': '_id',
                                'as':'region',
                                'pipeline': [
                                    {
                                        '$project':{
                                            'type':0,
                                            'coordinate':0,
                                            'acceptance_roles':0
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            '$unwind':'$region'
                        },
                        {
                            '$lookup':{
                                'from':'license_plate_in_and_out_time',
                                'localField':'_id',
                                'foreignField':'id_in_and_out',
                                'as':'in_and_out_times',
                                'pipeline':[
                                    {
                                        '$match':{'date':date}
                                    },
                                    # {
                                    #     '$project':{'times':0}
                                    # }
                                ]
                            },
                        }
                    ]
                }
            },
            {
                '$unwind':{
                    'path':'$in_and_out',
                    'preserveNullAndEmptyArrays':True
                }
            }
        ]
        result = self.db.mongodb[self.model].aggregate(pipeline)
        list = []
        ids_user = []
        async for data in result:
            list.append(data)
            if data['user_id'] != None:
                ids_user.append(str(data['user_id']))
        return list,ids_user

class RegionCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_region')

class InAndOutCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_in_and_out')
    
    async def add_in_and_out_list(self,data):
        await self.set_unique([('id_vehicle',1),('id_region',1)])
        ids = await self.add_many(data)
        return ids
    
    async def filter_detail_in_and_out_time(self,sort,skip,limit,search):
        technique = [ 
            {
                "$skip": (skip-1)*limit if skip > 0 else 0
            },
            {
                '$limit': limit
            }
        ]
        if sort != None:
            technique.append(
                {
                    '$sort': {"in_and_out_time.date": sort}
                },
            )
        pipeline = [
            {
                '$lookup':
                {
                    'from': 'license_plate_vehicle',
                    'localField':'id_vehicle',
                    'foreignField':'_id',
                    'as':'vehicle'
                },
            },{
                '$unwind':'$vehicle'
            },
            {
                '$lookup':
                {
                    'from': 'license_plate_region',
                    'localField':'id_region',
                    'foreignField':'_id',
                    'as':'region'
                },
            },
            {
                '$unwind':'$region'
            },
            {
                '$lookup':
                {
                    'from': 'license_plate_in_and_out_time',
                    'localField':'_id',
                    'foreignField':'id_in_and_out',
                    'pipeline': [
                        { '$project': {'id_in_and_out': 0 }}
                    ],
                    'as':'in_and_out_time'
                },
            },
            {
                '$unwind': '$in_and_out_time'
            }
        ]
        if search != None:
            if search.date!=None:
                pipeline.append(
                    {
                        '$match': {
                            'in_and_out_time.date':{
                                '$gte':search.date.start_date,'$lte':search.date.end_date
                            }
                        }
                    }
                )
            if search.time_in != None:
                pipeline.append(
                    {
                        '$match': {
                            'in_and_out_time.times':{
                                "$elemMatch":{
                                    'time':{
                                        '$gte':search.time_in.start_time,'$lte':search.time_in.end_time
                                    },
                                    'type':'in'
                                }
                            }
                        }
                    }
                )
            if search.time_out != None:
                pipeline.append(
                    {
                        '$match': {
                            'in_and_out_time.times':{
                                "$elemMatch":{
                                    'time':{
                                        '$gte':search.time_out.start_time,'$lte':search.time_out.end_time
                                    },
                                    'type':'out'
                                }
                            }
                        }
                    }
                )
            if search.region != None:
                if search.region.id_region != None:
                    pipeline.append(
                        {
                            '$match': {
                                'region._id':search.region.id_region
                            }
                        }
                    )
                if search.region.type != None:
                    pipeline.append(
                        {
                            '$match': {
                                'region.type':search.region.type
                            }
                        }
                    )
            if search.vehicle != None:
                if search.vehicle.user_id != None:
                    pipeline.append(
                        {
                            '$match':{
                                'vehicle.user_id':search.vehicle.user_id
                            }
                        }
                    )
                if search.vehicle.plate != None:
                    pipeline.append(
                        {
                            '$match':{
                                'vehicle.plate':search.vehicle.plate
                            }
                        }
                    )
                if search.vehicle.type != None:
                    pipeline.append(
                        {
                            '$match':{
                                'vehicle.type':search.vehicle.type
                            }
                        }
                    )
        pipeline.append(
            { '$facet': 
                {
                    'metadata': [
                        {   
                            '$group': { 
                                '_id': 'null',
                                'total': { '$sum': 1 },
                                'total_in_and_out':{
                                    '$sum':{
                                        '$size':"$in_and_out_time.times"
                                    }
                                },
                                'total_in':{
                                    '$sum':{
                                        '$size':{
                                                '$filter':{
                                                'input':"$in_and_out_time.times",
                                                'cond':{'$eq':['$$this.type','in']}
                                            }
                                        }
                                    }
                                },
                                'total_out':{
                                    '$sum':{
                                        '$size':{
                                            '$filter':{
                                                'input':"$in_and_out_time.times",
                                                'cond':{'$eq':['$$this.type','out']}
                                            }
                                        }
                                    }
                                }
                            },
                        },{
                            '$addFields':{'pages_size':0,'page':skip,'limit':limit}
                        }
                    ],
                    'list': technique
                }
            }
        )
        pipeline.append({
        '$project': { 
            'list': 1,
            'total': { '$arrayElemAt': [ '$metadata.total', 0 ] },
            'pages_size': { '$arrayElemAt': [ '$metadata.pages_size', 0 ] },
            'page': { '$arrayElemAt': [ '$metadata.page', 0 ] },
            'limit': { '$arrayElemAt': [ '$metadata.limit', 0 ] },
            'total_in_and_out':{'$arrayElemAt': [ '$metadata.total_in_and_out', 0 ]},
            'total_in':{'$arrayElemAt': [ '$metadata.total_in', 0 ]},
            'total_out':{'$arrayElemAt': [ '$metadata.total_out', 0 ]}
            }
        })
        result = self.db.mongodb[self.model].aggregate(
            pipeline
        )
        list = []
        async for data in result:
            # print(data)
            if data['list']==[]:
                list=data
            else:
                data['pages_size'] = math.ceil(data['total']/limit) if limit > 0 else 0
                list=data
        return list 

class InAndOutTimeCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_in_and_out_time')
    
    async def test_time(self):
        time = datetime.now(tz)
        return {"date":time.date(),"time":time.time()}
    
    async def create_query_index(self):
        index1 = IndexModel([('date',-1)])
        index2 = IndexModel([('times.time',-1)])
        await self.set_multi_key([index1,index2])
    
    async def push_times(self,ids,time):
        await self.db.mongodb[self.model].update_many(
            {
                self.key:{'$in': ids}
            },
            {
                '$push':{'times':time}
            }
        )
    
    async def create_in_and_out_time(self,data):
        await self.create_query_index()
        await self.add_many(data)
    
    async def show_total_in_and_out_time(self,date):
        pipeline = [
            {
                '$match': {
                    'date': date
                }
            },
            { '$facet': 
                {
                    'metadata': [
                        {   
                            '$group': { 
                                '_id': 'null',
                                'total_in_and_out':{
                                    '$sum':{
                                        '$size':"$times"
                                    }
                                },
                                'total_in':{
                                    '$sum':{
                                        '$size':{
                                                '$filter':{
                                                'input':"$times",
                                                'cond':{'$eq':['$$this.type','in']}
                                            }
                                        }
                                    }
                                },
                                'total_out':{
                                    '$sum':{
                                        '$size':{
                                            '$filter':{
                                                'input':"$times",
                                                'cond':{'$eq':['$$this.type','out']}
                                            }
                                        }
                                    }
                                }
                            },
                        },
                        {
                            '$addFields':{'date':date}
                        }
                    ],
                }
            },
            {
                '$project':{
                    'date':{'$arrayElemAt': [ '$metadata.date', 0 ]},
                    'total_in':{'$arrayElemAt': [ '$metadata.total_in', 0 ]},
                    'total_out':{'$arrayElemAt': [ '$metadata.total_out', 0 ]}
                }
            }
        ]
        
        result = self.db.mongodb[self.model].aggregate(
            pipeline
        )
        info = None
        async for data in result:
            info = data
            if info == {}:
                info['date'] = date
                info['total_in_and_out'] = 0
                info['total_in'] = 0
                info['total_out'] = 0
        return info