from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.Aluno import Aluno
from app.models.Administrador import Administrador
from app.models.Produto import Produto
from app.models.usuario_produto import UsuarioProduto
from app.models.Palestras_Eventos import PalestrasEventos
from app.models.Fase import Fase
from app.models.Atividade import Atividade

from .Mentoria_model import Mentoria
from .Entregavel_model import Entregavel