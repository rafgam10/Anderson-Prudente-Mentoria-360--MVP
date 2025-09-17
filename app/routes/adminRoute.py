from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from app.models import db, Administrador

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


#### Página Admin Principal

@admin_bp.route('/', methods=["GET"])
def index_admin():
    return render_template('baseAdm.html')


#### Gerenciamento de Administradores do Painel Admin.

@admin_bp.route('/admins/lista', methods=["GET"])
def lista_admins_page():
    return render_template('listaAdmins.html')

# @admin_bp.route('/admins/cadastro', methods=["GET","POST"])
# def cadastro_admins_page():
#     return render_template('cadastroAdmins.html')

@admin_bp.route('/admins/cadastro', methods=["GET","POST"])
def cadastro_admins():
    if request.method == "POST":
        nomeAdmin = request.form.get('nomeAdmin')
        emailAdmin = request.form.get('emailAdmin')
        senhaAdmin = request.form.get('senhaAdmin')
        
        adminObj = Administrador(
            nomeAdmin=nomeAdmin,
            emailAdmin=emailAdmin,
            senhaAdmin=senhaAdmin
        )
        print(f"Objeto criado DB: {adminObj}")
        db.session.add(adminObj)
        print(f"Adicionando na sessão...")
        db.session.commit()
        print("Commit - Admin adicionado com sucesso!")
        return redirect(url_for('admin.cadastro_admins'))  # nome do blueprint + função
    
    # Se for GET, apenas renderiza o template
    return render_template('cadastroAdmins.html')


##### Gerenciamento de Alunos no rota Admin.

@admin_bp.route('/alunos/lista', methods=["GET"])
def lista_alunos_page():
    return render_template('listaAlunos.html')


@admin_bp.route('/alunos/cadastro', methods=["GET","POST"])
def cadastro_aluno_page():
    return render_template('cadastroAlunos.html')


@admin_bp.route('/alunos/editar/<int:id>', methods=["PATCH"])
def editar_aluno(id:int):
    pass


@admin_bp.route('/alunos/deletar/<int:id>', methods=["DELETE"])
def deletar_aluno(id:int):
    pass