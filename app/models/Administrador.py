from flask_login import UserMixin
from app.models import db

class Administrador(db.Model, UserMixin):
    
    __tablename__ = "administradores"
    
    id = db.Column(db.Integer, primary_key=True)
    nomeAdmin = db.Column(db.String(255), nullable=False)
    emailAdmin = db.Column(db.String(255), nullable=False)
    senhaAdmin = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"Admin {self.id} - {self.nomeAdmin} - {self.senhaAdmin}"