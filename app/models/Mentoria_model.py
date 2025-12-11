from app.models import db
from app.models.associacoes import alunos_mentorias

class Mentoria(db.Model):
    
    __tablename__ = "mentorias"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_create = db.Column(db.Date, nullable=False)
    
    
    # Entregas
    entregaveis = db.relationship(
        "Entregavel",
        back_populates="mentoria",
        cascade="all, delete-orphan"
    )
    reunioes = db.relationship("Reuniao", back_populates="mentoria")
    
    alunos = db.relationship(
        "Aluno",
        secondary=alunos_mentorias,
        back_populates="mentorias"
    )
    
    def __init__(self, nome, descricao, data_create):
        self.nome = nome
        self.descricao = descricao
        self.data_create = data_create