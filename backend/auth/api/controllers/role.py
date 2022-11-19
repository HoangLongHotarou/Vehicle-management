from api.services.crud import RoleCrud, UserCrud
from utils.pyobjectid import PyObjectId
from utils.singleton import SingletonMeta
from db.database import get_database
import asyncio

db = asyncio.run(get_database())

app = 'auth'

class RoleController(metaclass=SingletonMeta):
    def __init__(self):
        self.db = db
        self.userCrud = UserCrud()
        self.roleCrud = RoleCrud()

    async def delete_role(self,id_role):
        async with await self.db.mongodb_client.start_session() as session:
            async with session.start_transaction():
                await self.roleCrud.delete(value=id_role,session=session)
                users,_ = await self.userCrud.get_all(query={'roles':PyObjectId(id_role)},projection={'_id':1})
                if users != []:
                    ids_users = [user['_id'] for user in users]
                    await self.userCrud.pull_role(ids_users, id_role, session)

    async def update_role(self,id_role,data):
        async with await self.db.mongodb_client.start_session() as session:
            async with session.start_transaction():
                await self.roleCrud.update(value=id_role, config_data=data.dict(),session=session)
                if data.users == [] or data.users == None: return
                users,_ = await self.userCrud.get_all(query={'$or':[{'_id':{'$in':data.users}},{'roles':PyObjectId(id_role)}]})
                push_role_users = []
                pull_role_users = []
                for user in users:
                    id_user = PyObjectId(user['_id'])
                    if id_user not in data.users and PyObjectId(id_role) in user['roles']:
                        pull_role_users.append(id_user)
                    if id_user in data.users and PyObjectId(id_role) not in user['roles']:
                        push_role_users.append(id_user)
                if pull_role_users != []:
                    await self.userCrud.pull_role(ids_user=pull_role_users, id_role=id_role,session=session)
                if push_role_users != []:
                    await self.userCrud.push_role(ids_user=push_role_users, id_role=id_role,session=session)