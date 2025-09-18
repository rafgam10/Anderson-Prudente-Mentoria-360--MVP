from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    request
)
from flask_login import (
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import check_password_hash
from app.models import db, Aluno, Administrador

login_bp = Blueprint("login", __name__, url_prefix='/login')

@login_bp.route("/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        inputEmailNome = request.form.get('InputUsuario')
        inputSenhaCpfAluno = request.form.get('InputSenha')
        
        # ADMIN
        user = Administrador.query.filter_by(emailAdmin=inputEmailNome).first()
        if user and check_password_hash(user.senhaAdmin, inputSenhaCpfAluno):
            login_user(user)
            flash("Login realizado como Admin!", "success")
            return redirect(url_for("admin.index_admin"))

        # ALUNO
        user = Aluno.query.filter_by(emailAluno=inputEmailNome).first()
        if user and user.senhaAluno == inputSenhaCpfAluno:
            login_user(user)
            flash("Login realizado como Aluno!", "success")
            return redirect(url_for("aluno.index_aluno"))

        flash("Usuário ou senha inválidos!", "error")
        return redirect(url_for('login.login_page'))

    # GET
    return render_template('login.html')

        
@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login_page'))
        
#####################################################################

@login_bp.route('/redireciona_login')
def redireciona_login():
    return redirect(url_for('login.login_page'))

#### Tem que fazer uma consulta com Banco de dados para validar Usuários
def validar_user_login(email: str, senha: str) -> bool:
    user = Administrador.query.filter_by(emailAdmin=email).first()
    if user and check_password_hash(user.senhaAdmin, senha):
        return user
    return None
    