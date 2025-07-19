import os 
import datetime



class Config(object):
    # =========================== SQLALCHEMY Settings ========================================
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://mosi:MOsi$324869@localhost/dashboard"
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    # SQLALCHEMY_TRACK_MODIFICATIONS = "False"
    
    # ========================================================================================
    UPLOAD_DIR = os.path.curdir + '/static/uploads/'
    SECRET_KEY = os.getenv('SECRET_KEY')
    # SECRET_KEY = "my_name_is_mostafa_ghorbani"

    # ======================= File Uploading ================================
    # UPLOAD_FOLDER = os.path.curdir + '/uploads'
    UPLOAD_FOLDER = os.path.curdir + '/static/uploads'
    # UPLOAD_FOLDER = '/static/uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB



class Development(Config):
    DEBUG = True


class Production(Config):
    DEBUG = False
    


