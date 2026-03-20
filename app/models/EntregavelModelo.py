from app.models import db

class EntregavelModelo(db.Model):
    __tablename__ = "entregaveis_modelo"
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), unique=True, nullable=False)
    
    def __init__(self, nome):
        self.nome = nome
