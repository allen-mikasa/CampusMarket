import os
import secrets

class Config:
    # 优先从环境变量获取SECRET_KEY，提高安全性
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(24)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # SQL Server数据库连接配置 - 优先从环境变量获取
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mssql+pyodbc://localhost/CampusMarket?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 修正上传文件夹路径
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static/uploads')
    # 限制文件上传大小为16MB
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # 文件扩展名限制
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}