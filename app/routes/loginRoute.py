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


@login_bp.route("/", endpoint="login_page")
def escolher_login():
    # exemplo: manda para o login de aluno
    return redirect(url_for("login.login_page_aluno"))



@login_bp.route("/aluno", methods=["GET", "POST"])
def login_page_aluno():
    if request.method == "POST":
        inputEmailNome = request.form.get('InputUsuario')
        inputSenhaCpfAluno = request.form.get('InputSenha')
        print("Pegado dados do Login - Aluno")
        
        # ALUNO
        user = Aluno.query.filter_by(emailAluno=inputEmailNome).first()
        print("Aluno encontrado:", user)
        # if user and check_password_hash(user.senhaAluno, inputSenhaCpfAluno):#user.senhaAluno == inputSenhaCpfAluno
        if user and inputSenhaCpfAluno == user.senhaAluno or inputSenhaCpfAluno == user.CPFAluno:
            logout_user()
            login_user(user)
            flash("Login realizado como Aluno!", "success")
            return redirect(url_for("aluno.index_aluno"))
        
        elif user and check_password_hash(user.senhaAluno, inputSenhaCpfAluno) or check_password_hash(user.CPFAluno, inputSenhaCpfAluno):
            login_user(user)
            flash("Login realizado como Aluno!", "success")
            return redirect(url_for("aluno.index_aluno"))

        flash("Usuário ou senha inválidos!", "error")
        print("Não entrou no Login")
        return redirect(url_for('login.login_page_aluno'))

    # GET
    return render_template('loginAlunos.html')


@login_bp.route("/admin", methods=["GET", "POST"])
def login_page_admin():
    if request.method == "POST":
        inputEmailNome = request.form.get('InputUsuario')
        inputSenhaCpfAluno = request.form.get('InputSenha')
        print("Pegado dados do Login - Admin")
        
        # ADMIN
        user = Administrador.query.filter_by(emailAdmin=inputEmailNome).first()
        print("Admin encontrado:", user)
        if user and user.senhaAdmin == inputSenhaCpfAluno:
            login_user(user)
            print("Acesso ao Admin")
            flash("Login realizado como Admin!", "success")
            session["nomeAdmin"] = user.nomeAdmin
            return redirect(url_for("admin.index_admin"))
        
        elif user and check_password_hash(user.senhaAdmin, inputSenhaCpfAluno):
            login_user(user)
            print("Acesso ao Admin")
            flash("Login realizado como Admin!", "success")
            return redirect(url_for("admin.index_admin"))
        
        flash("Usuário ou senha inválidos!", "error")
        print("Não entrou no Login")
        return redirect(url_for('login.login_page_admin'))
        
    # GET
    return render_template('loginAdmin.html')
        
@login_bp.route('/logout')
@login_required
def logout():
    
    if isinstance(current_user, Aluno):
        logout_user()
        flash("Logout realizado com sucesso (Aluno)!", "success")
        return redirect(url_for('login.login_page_aluno'))
    
    if isinstance(current_user, Administrador):
        logout_user()
        flash("Logout realizado com sucesso (Admin)!", "success")
        return redirect(url_for('login.login_page_admin'))
    
    logout_user()
    return redirect(url_for('login.login_page_aluno'))
        
#####################################################################

@login_bp.route('/redireciona_login')
def redireciona_login():
    return redirect(url_for('login.login_page_aluno'))

#### Tem que fazer uma consulta com Banco de dados para validar Usuários
def validar_user_login(email: str, senha: str) -> bool:
    user = Administrador.query.filter_by(emailAdmin=email).first()
    if user and check_password_hash(user.senhaAdmin, senha):
        return user
    return None
    