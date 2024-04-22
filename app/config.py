from dotenv import load_dotenv
from os import environ

load_dotenv()


class Config:
    SECRET_KEY = environ.get('SECRET_KEY')
    GOOGLE_CLIENT_ID = environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = environ.get('GOOGLE_CLIENT_SECRET')
