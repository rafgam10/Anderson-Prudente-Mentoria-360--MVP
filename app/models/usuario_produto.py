from app.models import db

class UsuarioProduto(db.Model):
    
    __tablename__ = "usuarios_produtos"
    
    usuario_id = db.Column(
        db.Integer, 
        db.ForeignKey("alunos.id", ondelete="CASCADE"),
        primary_key=True
    )
    produto_id = db.Column(
        db.Integer, 
        db.ForeignKey("produtos.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    aluno = db.relationship(
        "Aluno", 
        backref=db.backref(
            "produtos_assoc", 
            cascade="all, delete-orphan")
    )
    produto = db.relationship(
        "Produto", 
        backref=db.backref(
            "usuarios_assoc", 
            cascade="all, delete-orphan")
    )