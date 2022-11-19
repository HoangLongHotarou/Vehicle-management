import math
import asyncio

from fastapi import HTTPException, Request
from utils.pyobjectid import PyObjectId
from utils.singleton import SingletonMeta

from .schema import PaginationInfo
from db.database import get_database

db = asyncio.run(get_database())

class BaseCrud(metaclass=SingletonMeta):
    '''
        model: Name of collection for mongodb
        request: Request from mongodb (AsyncIOMotorClient)
        key: key of document (default '_id')
    '''

    def __init__(self, model: str, key='_id') -> None:
        self.model = model
        self.db = db
        self.key = key

    async def set_unique(self, select: list):
        await self.db.mongodb[self.model].create_index(select, unique=True)

    async def set_multi_key(self, select: list):
        await self.db.mongodb[self.model].create_indexes(select)

    async def add(self, data: dict, session=None):
        '''
            Add data to database
            ----------------------------------------------------------------
            data: data request from client (must convert data to dictionary)
            session: use transaction (default None if not use transaction)
            ----------------------------------------------------------------
        '''
        if self.key != '_id':
            await self.db.mongodb[self.model].create_index(self.key, unique=True)
        try:
            data = await self.db.mongodb[self.model].insert_one(data, session=session)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f'{e}')
        new_data = await self.get(value=data.inserted_id, session=session)
        return new_data

    async def get(self, **kwargs):
        '''
            Get database follow primary key or query
            -----------------------------------------------------------
            choose either value or query to get document
            value: value for primary key
            query: query for document (example: {key:value})
            -----------------------------------------------------------
            projection: manually select the specified field in the document
            session: use transaction
            -----------------------------------------------------------
        '''
        value = kwargs.get('value')
        query = kwargs.get('query')
        exception = kwargs.get('exception', False)
        projection = kwargs.get('projection')
        session = kwargs.get('session')
        query_db = {}
        if value:
            if self.key == '_id':
                try:
                    value = PyObjectId(value)
                except:
                    raise HTTPException(status_code=404, detail="invalid id")
            query_db = {self.key: value}
        elif query:
            query_db = query
        else:
            raise HTTPException(
                status_code=404, detail=f"missing parameter query or value")
        data = await self.db.mongodb[self.model].find_one(query_db, projection=projection, session=session)
        if data is None and value is not None:
            raise HTTPException(
                status_code=404, detail=f"Could not find: {value} for model: '{self.model}'")
        return data

    async def get_all(self, **kwargs):
        '''
            Get all database follow query
            -----------------------------------------------------------
            query: query for document (example: {key:value})
            limit, page: use for pagination
            sort: sort ascending or descending
            is_get_info: get information
            -----------------------------------------------------------
        '''
        data_list = []
        info = None
        query = kwargs.get('query', {})
        limit = kwargs.get('limit', 0)
        page = kwargs.get('page', 0)
        sort = kwargs.get('sort', [])
        is_get_info = kwargs.get('is_get_info', False)
        projection = kwargs.get('projection')
        list = self.db.mongodb[self.model].find(
            query,
            limit=limit,
            skip=(page-1)*limit if page > 0 else 0,
            projection=projection
        )
        if sort != []:
            list = list.sort(sort)
        async for data in list:
            data_list.append(data)
        if is_get_info == True:
            total = await self.size_collections(query=query)
            pages_size = math.ceil(total/limit) if limit > 0 else 0
            info = PaginationInfo(
                total=total, pages_size=pages_size, page=page, limit=limit)
        return data_list, info

    async def update(self, value: str, config_data: dict, session=None):
        '''
            Update database follow value
            -----------------------------------------------------------
            value: value for primary key
            config_data: modify data for database
            session: use transaction
            -----------------------------------------------------------
        '''
        update_data = None
        data = await self.get(value=value)
        for key in config_data:
            if config_data[key] is None:
                continue
            data[key] = config_data[key]
        try:
            update_data = await self.db.mongodb[self.model].update_one(
                {
                    self.key: input if self.key != '_id' else PyObjectId(value)
                },
                {
                    "$set": data
                },
                session=session
            )
        except Exception as e:
            raise HTTPException(status_code=422, detail=f'{e}')
        return update_data.modified_count == 1

    async def delete(self, **kwargs):
        '''
            Delete database follow value or array
            -----------------------------------------------------------
            value: for primary key
            array: for primary key
            session: use transaction
            -----------------------------------------------------------
        '''
        value = kwargs.get('value')
        array = kwargs.get('array')
        session = kwargs.get('session')
        if value:
            data = await self.get(value=value)
            await self.db.mongodb[self.model].delete_one(
                {
                    self.key: value if self.key != '_id' else PyObjectId(value)
                },
                session=session
            )
        elif array:
            await self.db.mongodb[self.model].delete_many(
                {
                    self.key: {'$in': array}
                },
                session=session
            )

    async def size_collections(self, query):
        return await self.db.mongodb[self.model].count_documents(query)
