from app.models import db

class AlunoEntregavel(db.Model):
    __tablename__ = "alunos_entregaveis"
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey("alunos.id"), nullable=False)
    entregavel_id = db.Column(db.Integer, db.ForeignKey("entregaveis.id"), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pendente')
    data_entrega = db.Column(db.Date, nullable=True)
    
    # Relações
    aluno = db.relationship("Aluno", back_populates="entregaveis_status")
    entregavel_template = db.relationship("Entregavel")

    def __repr__(self):
        return f"<AlunoEntregavel Aluno:{self.aluno_id} Entregável:{self.entregavel_id} Status:{self.status}>"
