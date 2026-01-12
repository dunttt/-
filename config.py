import os
from datetime import timedelta

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB配置
    MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.environ.get('MONGODB_PORT', 27017))
    MONGODB_USER = os.environ.get('MONGODB_USER', '')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD', '')
    MONGODB_DB = os.environ.get('MONGODB_DB', 'novel_platform')
    
    # 构建MongoDB连接URI
    if MONGODB_USER and MONGODB_PASSWORD:
        # Docker 模式：带认证
        MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}?authSource=admin"
    else:
        # 本地模式：无认证
        MONGODB_URI = f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DB}"
    
    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # 文件上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    
    # 分页配置
    NOVELS_PER_PAGE = 12
    COMMENTS_PER_PAGE = 10
