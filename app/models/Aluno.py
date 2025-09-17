from models import db

class Aluno(db.Model):
    
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nomeAluno = db.Column(db.String(100), nullable=False)
    emailAluno = db.COlumn(db.String(255), nullable=False)
    senhaAluno = db.Column(db.String(255), nullable=False)
    CPFAluno = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f"<Aluno {self.nomeAluno}>"