import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'RISHAV24'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizapp.db'  # Or your database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False