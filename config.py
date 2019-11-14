'''Flask config class'''
import os


class Config:
    '''Set Flask configuration variables from .env file'''
    
    # General
    TESTING = os.getenv('TESTING')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database
    MONGO_URI = os.getenv('MONGO_URI')
    