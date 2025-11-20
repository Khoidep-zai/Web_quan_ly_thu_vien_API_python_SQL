import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    # Sử dụng SQLite cho development nếu không có PostgreSQL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback to SQLite
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "..", "library.db")}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)

    # APScheduler
    SCHEDULER_API_ENABLED = True

    # Application specific
    BORROW_DAYS_DEFAULT = int(os.environ.get('BORROW_DAYS_DEFAULT', 14))
    REMINDER_DAYS_BEFORE = int(os.environ.get('REMINDER_DAYS_BEFORE', 3))
    PER_PAGE = int(os.environ.get('PER_PAGE', 20))
    FINE_PER_DAY = float(os.environ.get('FINE_PER_DAY', 0.5))  # Phí trễ hạn mỗi ngày (VNĐ)
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(basedir, '..', 'static', 'uploads', 'books')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
