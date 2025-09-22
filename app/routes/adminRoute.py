from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Administrador, Aluno, Produto

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


#### Página Admin Principal
@admin_bp.route('/home', methods=["GET"])
def index_admin():
    return render_template('homeAdmin.html')


#### Gerenciamento de Administradores do Painel Admin.

@admin_bp.route('/admins/lista', methods=["GET"])
def lista_admins():
    array_admin = list(Administrador.query.all())
    return render_template('listaAdmins.html', lista_admin=array_admin)

@admin_bp.route('/admins/cadastro', methods=["GET","POST"])
def cadastro_admins():
    if request.method == "POST":
        nomeAdminInput = request.form.get('nomeAdmin')
        emailAdminInput = request.form.get('emailAdmin')
        senhaAdminInput = generate_password_hash(request.form.get('senhaAdmin'))
        
        novo_Admin = Administrador(
            nomeAdmin=nomeAdminInput, 
            emailAdmin=emailAdminInput,
            senhaAdmin=generate_password_hash(senhaAdminInput)
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


@admin_bp.route('/admins/editar/<int:id>', methods=["PATCH"])
def editar_admin(id:int):
    pass


@admin_bp.route('/admins/deletar/<int:id>', methods=["DELETE"])
def deletar_admin(id:int):
    pass

##### Gerenciamento de Alunos no rota Admin.

@admin_bp.route('/alunos/lista', methods=["GET"])
def lista_alunos():
    array_alunos = Aluno.query.all()
    return render_template('listaAlunos.html', array_alunos=array_alunos)


@admin_bp.route('/alunos/cadastro', methods=["GET","POST"])
def cadastro_aluno():
    if request.method == "POST":
        
        inputNomeAluno = request.form.get('nomeAluno')
        inputEmailAluno = request.form.get('emailAluno')
        inputSenhaAluno = request.form.get('senhaAluno')
        inputCPFAluno = request.form.get('cpfAluno')
        
        produtos_marcados = request.form.getlist('produtos')
        
        # Exibir dados coletados.
        print("Nome:", inputNomeAluno)
        print("Email:", inputEmailAluno)
        print("Senha:", inputSenhaAluno)
        print("CPF:", inputCPFAluno)
        print("Produtos selecionados:", produtos_marcados)
        
        # Inserir alunos no DB:
        novo_aluno = Aluno(
            nomeAluno=inputNomeAluno,
            emailAluno=inputEmailAluno,
            senhaAluno=generate_password_hash(inputSenhaAluno),
            CPFAluno=inputCPFAluno
        )
            
        # Busca os produtos selecionado no DB:
        if produtos_marcados:
            produtos_db = Produto.query.filter(Produto.nomeProduto.in_(produtos_marcados)).all()
            novo_aluno.produtos.extend(produtos_db)
            print("Produtos do aluno:",produtos_db, " - ", produtos_marcados)
            
        
        db.session.add(novo_aluno)
        db.session.commit()
        print("Registro inserido no Banco de dados...")
        
        flash(f"Aluno {inputNomeAluno} cadastrado com sucesso!", "success")
        return redirect(url_for('admin.cadastro_aluno'))
    
    return render_template('cadastroAlunos.html')


@admin_bp.route('/alunos/editar/<int:id>', methods=["PATCH"])
def editar_aluno(id:int):
    pass


@admin_bp.route('/alunos/deletar/<int:id>', methods=["DELETE"])
def deletar_aluno(id:int):
    pass