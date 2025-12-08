from app.models import db

class Produto(db.Model):
    
    __tablename__ = "produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    nomeProduto = db.Column(db.String(100), nullable=False, unique=True)
    
    alunos = db.relationship(
        "Aluno", 
        secondary="usuarios_produtos", 
        back_populates="produtos"
    )
    
    
    def __repr__(self):
        return f"Produto {self.id} - {self.nomeProduto}"