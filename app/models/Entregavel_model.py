from app.models import db

class Entregavel(db.Model):
    
    __tablename__ = "entregaveis"
    
    id = db.Column(db.Integer, primary_key=True)
    id_mentoria = db.Column(
        db.Integer, 
        db.ForeignKey("mentorias.id"), 
        nullable=False
    )
    nome = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')
    data_entrega = db.Column(db.Date, nullable=True)
    
    # Relações
    mentoria = db.relationship("Mentoria", back_populates="entregaveis")
