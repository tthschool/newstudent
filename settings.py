import os
from dotenv import load_dotenv

# Load các biến môi trường từ tệp .env
load_dotenv()

# Sử dụng các biến môi trường đã load
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
