from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import (
    db,
    Aluno,
    Produto,
    PalestrasEventos,
    Atividade,
    Fase
)

aluno_bp = Blueprint("aluno", __name__,url_prefix='/aluno')


@aluno_bp.route('/home', methods=["GET"])
@login_required
def index_aluno():
    # Garante que só alunos acessem
    # if not isinstance(current_user, Aluno):
    #     flash("Você não tem permissão para acessar essa página!", "error")
    #     return redirect(url_for("admin.index_admin"))

    aluno = Aluno.query.get(current_user.id)
    print(f"Aluno logado ID: {aluno.id}")

    # Pega todos os cursos
    todos_cursos = Produto.query.all()
    
    # Supondo que cursos_aluno seja a lista de cursos que o aluno desbloqueou
    cursos_aluno = aluno.produtos  # ajuste conforme seu relacionamento
    desbloqueados = cursos_aluno
    bloqueados = [curso for curso in todos_cursos if curso not in cursos_aluno]


    # Lista de eventos que terão:
    eventos = PalestrasEventos.query.all()
    
    #MPS
    atividades_mps = (
        db.session.query(Atividade)
        .join(Fase)
        .filter(Atividade.plataforma == "MPS")
        .order_by(Fase.id_fase.asc(), Atividade.id.asc())
        .all()
    )
    
    #DOP
    atividades_dop = (
        db.session.query(Atividade)
        .join(Fase)
        .filter(Atividade.plataforma == "DOP")
        .order_by(Fase.id_fase.asc(), Atividade.id.asc())
        .all()
    )

    return render_template(
        "homeAlunos.html",
        desbloqueados=desbloqueados,
        bloqueados=bloqueados,
        aluno=aluno,
        eventos=eventos,
        atividades_dop=atividades_dop,
        atividades_mps=atividades_mps
    )



#### Mapa mental do BOP para visualização.
@aluno_bp.route('/cursos1', methods=["GET"])
def cursos_page1():
    
    return render_template("")

#### Mapa mental da MPS para visualização.
@aluno_bp.route('/cursos2', methods=["GET"])
def cursos_page2():
    
    return render_template("")

##### Ver o desempenho, tarefas, datas de paletras.
@aluno_bp.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("")


@aluno_bp.route('/conta', methods=["GET"])
def conta_page():
    
    return render_template("")

@aluno_bp.route('/perfil', methods=["GET"])
def perfil_page():
    
    return render_template("")





