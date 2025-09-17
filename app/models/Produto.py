from models import db

class Produto(db.Model):
    
    __tablename__ = "produtos"
    
    id = db.Column(db.Integer, primary_key=True)
    nomeProduto = db.Column(db.String(100), nullable=False)