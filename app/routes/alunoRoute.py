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
from app.models import db, Aluno, Produto

aluno_bp = Blueprint("aluno", __name__,url_prefix='/aluno')


@aluno_bp.route('/home', methods=["GET"])
def index_aluno():
    
    # Aqui fica a página principal com uma Navbar no centro dos produtos.
    cursos_aluno = current_user.produtos
    
    todos_cursos = Produto.query.all()
    
    desbloqueados = cursos_aluno
    bloqueados = [curso for curso in todos_cursos if curso not in cursos_aluno]
    
    
    return render_template("homeAlunos.html",
                           desbloqueados=desbloqueados,
                           bloqueados=bloqueados)
    
    # return render_template("homeAlunos.html")


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





