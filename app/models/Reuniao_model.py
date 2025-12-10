from app.models import db

class Reuniao(db.Model):
    
    __tablename__ = "reunioes"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    
    
    id_mentoria = db.Column(db.Integer, db.ForeignKey('mentorias.id'), nullable=False)
    id_aluno = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    
    # Relação
    aluno = db.relationship("Aluno", back_populates="reunioes")
    mentoria = db.relationship("Mentoria", back_populates="reunioes")
    
    def __init__(self, nome, data, id_mentoria, id_aluno):
        self.nome = nome
        self.data = data
        self.id_mentoria = id_mentoria
        self.id_aluno = id_aluno