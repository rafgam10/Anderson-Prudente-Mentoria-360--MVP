from flask_login import UserMixin
from app.models import db

class PalestrasEventos(db.Model, UserMixin):
    
    __tablename__ = 'palestras_eventos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeEvento = db.Column(db.String(255), nullable=False)
    dataInicial = db.Column(db.Date, nullable=False)
    dataFinal = db.Column(db.Date, nullable=False)
    nomePalestrate = db.Column(db.String(150), nullable=False)
    
    def __repr__(self):
        return f"<Aluno {self.nomeEvento} - {self.nomePalestrate}>"