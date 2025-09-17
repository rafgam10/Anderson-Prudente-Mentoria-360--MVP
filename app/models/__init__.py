from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.Aluno import Aluno
from app.models.Administrador import Administrador
from app.models.Produto import Produto
from app.models.usuario_produto import UsuarioProduto