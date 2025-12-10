from flask_login import UserMixin
from app.models import db

class Aluno(db.Model, UserMixin):
    
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nomeAluno = db.Column(db.String(255), nullable=False)
    emailAluno = db.Column(db.String(255), nullable=False)
    senhaAluno = db.Column(db.String(255), nullable=False)
    CPFAluno = db.Column(db.String(255), nullable=False)
    
    produtos = db.relationship("Produto", secondary="usuarios_produtos", back_populates="alunos")
    reunioes = db.relationship("Reuniao", back_populates="aluno")
    
    def __repr__(self):
        return f"<Aluno {self.nomeAluno}>"