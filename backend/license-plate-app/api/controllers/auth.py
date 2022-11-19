from api.services.fetchapi import FetchAuthAPI
from utils.singleton import SingletonMeta


class AuthController(metaclass=SingletonMeta):
    def __init__(self):
        self.fetchAuth = FetchAuthAPI() 
    
    def login(self,user):
        return self.fetchAuth.login(user)