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
    
    mentoria_id = db.Column(db.Integer, db.ForeignKey("mentorias.id"), nullable=True)
    
    produtos = db.relationship("Produto", secondary="usuarios_produtos", back_populates="alunos")
    reunioes = db.relationship("Reuniao", back_populates="aluno", cascade="all, delete-orphan")
    mentoria = db.relationship("Mentoria", back_populates="alunos")
    entregaveis_status = db.relationship("AlunoEntregavel", back_populates="aluno", cascade="all, delete-orphan")
    
    @property
    def ultima_reuniao(self):
        if not self.reunioes:
            return None
        return max(reuniao.data for reuniao in self.reunioes)
    
    @property
    def entregaveis(self):
        # Retorna os registros de status específicos deste aluno
        return self.entregaveis_status
    
    def __repr__(self):
        return f"<Aluno {self.nomeAluno}>"