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
    
    
    
    
    mentoria = db.relationship("Mentoria", back_populates="entregaveis")