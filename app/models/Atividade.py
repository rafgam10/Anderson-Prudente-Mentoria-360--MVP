from flask_login import UserMixin
from app.models import db

class Atividade(db.Model, UserMixin):
    __tablename__ = "atividades"

    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    plataforma = db.Column(db.String(50), nullable=False)

    fase_id = db.Column(db.Integer, db.ForeignKey("fases.id_fase"), nullable=False)
    fase = db.relationship("Fase", back_populates="atividades")

    def __repr__(self):
        return f"<Atividade {self.id} - {self.nome_atividade}>"   