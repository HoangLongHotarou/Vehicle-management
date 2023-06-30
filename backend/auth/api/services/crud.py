from base.crud import BaseCrud
from pymongo import IndexModel
from utils.pyobjectid import PyObjectId

app = 'auth'


class OTPCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_otp')

    async def create_expire(self):
        await self.db.mongodb[self.model].create_index('created_at', expireAfterSeconds=120)

    async def add(self, data, session=None):
        await self.create_expire()
        return await super().add(data, session=session)


class UserCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_user')

    async def set_multi_unique(self):
        index1 = IndexModel([('username', 1)], unique=True)
        index2 = IndexModel([('email', 1)], unique=True)
        index3 = IndexModel([('phone_number', 1)], unique=True)
        await self.set_multi_key([index1, index2, index3])

    async def pull_role(self, ids_user, id_role, session):
        await self.db.mongodb[self.model].update_many({self.key: {'$in': ids_user}}, {'$pull': {'roles': PyObjectId(id_role)}}, session=session)

    async def push_role(self, ids_user, id_role, session):
        await self.db.mongodb[self.model].update_many({self.key: {'$in': ids_user}}, {'$push': {'roles': PyObjectId(id_role)}}, session=session)


class RoleCrud(BaseCrud):
    def __init__(self):
        super().__init__(f'{app}_role')

    async def pull_user(self, ids_role, id_user, session):
        await self.db.mongodb[self.model].update_many({self.key: {'$in': ids_role}}, {'$pull': {'users': PyObjectId(id_user)}}, session=session)

    async def push_user(self, ids_role, id_user, session):
        await self.db.mongodb[self.model].update_many({self.key: {'$in': ids_role}}, {'$push': {'users': PyObjectId(id_user)}}, session=session)

    async def get_role_detail(self, id_role):
        pipeline = [
            {
                '$match': {
                    '_id': PyObjectId(id_role)
                }
            },
            {
                '$lookup': {
                    'from': 'user',
                    'localField': 'users',
                    'foreignField': '_id',
                    'as': 'users',
                    # 'pipeline': [/
                },
            },
        ]
        result = await self.db.mongodb[self.model].aggregate(
            pipeline
        )
        role_detail = {}
        async for data in result:
            role_detail=data
        return role_detail