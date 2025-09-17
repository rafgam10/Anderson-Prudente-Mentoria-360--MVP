from models import db

class Administrador(db.Model):
    
    __tablename__ = "administradores"
    
    id = db.Column(db.Integer, primary_key=True)
    nomeAdmin = db.Column(db.Integer, nullable=False)
    senhaAdmin = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Admin {self.id} - {self.nomeAdmin} - {self.senhaAdmin}"