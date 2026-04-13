import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret')

    # MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'db')
    MYSQL_USER = os.getenv('MYSQL_USER', 'eventflow_user')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'eventflow_pass')
    MYSQL_DB = os.getenv('MYSQL_DB', 'eventflow_db')
    MYSQL_CURSORCLASS = 'DictCursor'

    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB limit
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}