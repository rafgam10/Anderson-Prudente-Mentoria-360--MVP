

# Variaveis do Mysql
USER = "root"
PASSWORD = "root"
HOST = "localhost"
DB_NAME = "mentoria360_mvp"


SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False # Recommended to disable