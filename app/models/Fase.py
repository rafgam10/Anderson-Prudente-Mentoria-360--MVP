from flask_login import UserMixin
from app.models import db

class Fase(db.Model, UserMixin):
    __tablename__ = "fases"

    id_fase = db.Column(db.Integer, primary_key=True)
    nome_fase = db.Column(db.String(100), nullable=False)

    atividades = db.relationship("Atividade", back_populates="fase", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Fase {self.id_fase} - {self.nome_fase}>"