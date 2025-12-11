from app.models import db

alunos_mentorias = db.Table(
    "alunos_mentorias",
    db.Column("aluno_id", db.Integer, db.ForeignKey("alunos.id"), primary_key=True),
    db.Column("mentoria_id", db.Integer, db.ForeignKey("mentorias.id"), primary_key=True)
)
