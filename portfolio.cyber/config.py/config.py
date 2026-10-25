import os 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cyver_secret_key_9988_tech'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False