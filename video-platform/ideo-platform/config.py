import os
from dotenv import load_dotenv
load_dotenv()
class Config:
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_PREFIX = os.getenv('S3_PREFIX', 'uploads')
UPLOAD_FOLDER = 'uploads'
