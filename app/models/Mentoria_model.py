from app.models import db

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