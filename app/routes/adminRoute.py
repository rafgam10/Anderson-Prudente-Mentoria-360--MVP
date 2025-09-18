from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Administrador

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


#### Página Admin Principal
@admin_bp.route('/', methods=["GET"])
def index_admin():
    return render_template('homeAdmin.html')


#### Gerenciamento de Administradores do Painel Admin.

@admin_bp.route('/admins/lista', methods=["GET"])
def lista_admins():
    return render_template('listaAdmins.html')

@admin_bp.route('/admins/cadastro', methods=["GET","POST"])
def cadastro_admins():
    if request.method == "POST":
        nomeAdminInput = request.form.get('nomeAdmin')
        emailAdminInput = request.form.get('emailAdmin')
        senhaAdminInput = generate_password_hash(request.form.get('senhaAdmin'))
        
        novo_Admin = Administrador(
            nomeAdmin=nomeAdminInput, 
            emailAdmin=emailAdminInput,
            senhaAdmin=senhaAdminInput
        )
        print("Obj Admin criando...")
        
        try:
            db.session.add(novo_Admin)
            db.session.commit()
            print("Commit OK!")
        except Exception as e:
            db.session.rollback()
            print("Erro ao salvar:", e)

        
        flash("Novo Administrador criado com sucesso!", "success")
        return redirect(url_for('admin.cadastro_admins'))
    
    # GET
    return render_template('cadastroAdmins.html')



##### Gerenciamento de Alunos no rota Admin.

@admin_bp.route('/alunos/lista', methods=["GET"])
def lista_alunos():
    return render_template('listaAlunos.html')


@admin_bp.route('/alunos/cadastro', methods=["GET","POST"])
def cadastro_aluno():
    if request.method == "POST":
        
        inputNomeAluno = request.form.get('nomeAluno')
        inputEmailAluno = request.form.get('emailAluno')
        inputSenhaAluno = request.form.get('senhaAluno')
        inputCPFAluno = request.form.get('cpfAluno')
        
    
    return render_template('cadastroAlunos.html')


@admin_bp.route('/alunos/editar/<int:id>', methods=["PATCH"])
def editar_aluno(id:int):
    pass


@admin_bp.route('/alunos/deletar/<int:id>', methods=["DELETE"])
def deletar_aluno(id:int):
    pass