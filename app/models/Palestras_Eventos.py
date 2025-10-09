from flask_login import UserMixin
from app.models import db

class PalestrasEventos(db.Model, UserMixin):
    
    __tablename__ = 'palestras_eventos'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeEvento = db.Column(db.String(255), nullable=False)
    dataInicial = db.Column(db.Date, nullable=False)
    horaInicial = db.Column(db.Time, nullable=False)
    dataFinal = db.Column(db.Date, nullable=False)
    horaFinal = db.Column(db.Time, nullable=False)
    nomePalestrante = db.Column(db.String(150), nullable=False)  # ✅ corrigido
    
    def __repr__(self):
        return f"<Evento {self.nomeEvento} - {self.nomePalestrante}>"
