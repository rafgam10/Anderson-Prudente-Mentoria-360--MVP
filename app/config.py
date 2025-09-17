import os 

USER = "root"
PASSWORD = "root"
HOST = "localhost"
DB_NAME = "mentoria360_mvp"


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False # Recommended to disable