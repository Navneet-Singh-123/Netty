import json
from operator import index
from cryptography.fernet import Fernet
from ..models import User
from ..serializers import UserSerializer
from rest_framework.decorators import api_view
import environ

env = environ.Env()
environ.Env.read_env()


# Authentication using netty
class NettyAuth:
 
    def __init__(self, user_id="", username="", password=""):
        self.user_id = user_id
        self.username = username
        self.password = password

    def encrypt(self):
        key = bytes(env("SECRET_KEY"), 'utf-8')
        fernet = Fernet(key)
        encPassword = fernet.encrypt(self.password.encode())
        return encPassword

    def decrypt(self, encPassword):
        byt_pas = bytes(encPassword, 'utf-8')           
        key = bytes(env("SECRET_KEY"), 'utf-8')        
        fernet = Fernet(key)
        decPassword = fernet.decrypt(byt_pas).decode()
        return decPassword
