from flask_login import UserMixin
from app.models import db
from app.models.associacoes import alunos_mentorias

class Aluno(db.Model, UserMixin):
    
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nomeAluno = db.Column(db.String(255), nullable=False)
    emailAluno = db.Column(db.String(255), nullable=False)
    senhaAluno = db.Column(db.String(255), nullable=False)
    CPFAluno = db.Column(db.String(255), nullable=False)
    
    produtos = db.relationship("Produto", secondary="usuarios_produtos", back_populates="alunos")
    reunioes = db.relationship("Reuniao", back_populates="aluno")
    mentorias = db.relationship("Mentoria", secondary=alunos_mentorias, back_populates="alunos")
    
    @property
    def ultima_reuniao(self):
        if not self.reunioes:
            return None
        return max(reuniao.data for reuniao in self.reunioes)
    
    @property
    def entregaveis(self):
        entregaveis = []
        for mentoria in self.mentorias:
            entregaveis.extend(mentoria.entregaveis)
        return entregaveis
    
    def __repr__(self):
        return f"<Aluno {self.nomeAluno}>"