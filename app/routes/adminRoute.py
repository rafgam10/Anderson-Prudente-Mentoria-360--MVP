from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    jsonify,
    request
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Administrador, Aluno, Produto, PalestrasEventos
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


#### Página Admin Principal
@admin_bp.route('/home', methods=["GET"])
def index_admin():
    return render_template('homeAdmin.html')

###########################################################
#### Gerenciamento de Administradores do Painel Admin.#####
###########################################################

@admin_bp.route('/admins/lista', methods=["GET"])
def lista_admins():
    array_admin = list(Administrador.query.all())
    return render_template('listaAdmins.html', lista_admin=array_admin)

@admin_bp.route('/admins/cadastro', methods=["GET","POST"])
def cadastro_admins():
    if request.method == "POST":
        nomeAdminInput = request.form.get('nomeAdmin')
        emailAdminInput = request.form.get('emailAdmin')
        senhaAdminInput = request.form.get('senhaAdmin')
        
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
def editar_admin(id:int) -> None:
    data = request.get_json()
    
    admin = Administrador.query.get(id)
    if not admin:
        return jsonify({"error": "Administrador não encontrado"}), 404
    
    admin.nomeAdmin = data.get("nome", admin.nomeAdmin)
    admin.emailAdmin = data.get("email", admin.emailAdmin)
    
    if data.get("senha"):
        admin.senhaAdmin = generate_password_hash(data["senha"])
    
    try:
        db.session.commit()
        print(f"Admin atualizado com sucesso")
        return jsonify({"message": "Administrador atualizado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao atualizar administrador: {str(e)}"}), 500



@admin_bp.route('/admins/deletar/<int:id>', methods=["DELETE"])
def deletar_admin(id:int):
    admin = Administrador.query.get(id)
    if not admin:
        return jsonify({"error": "Administrador não encontrado"}), 404
    
    try:
        db.session.delete(admin)
        db.session.commit()
        print("Admin Removido com Sucesso no DB!")
        return jsonify({"message": "Administrador deletado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar administrador: {str(e)}"}), 500
        

#################################################
##### Gerenciamento de Alunos no rota Admin.#####
#################################################

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
def editar_aluno(id:int) -> None:
    data = request.get_json()
    
    aluno = Aluno.query.get_or_404(id)
    
    aluno.nomeAluno = data.get("nome", aluno.nomeAluno)
    aluno.emailAluno = data.get("email", aluno.emailAluno)
    aluno.CPFAluno = data.get("cpf", aluno.CPFAluno)
    
    produto_input = data.get("produto")
    aluno.produtos.clear()
    
    if produto_input:
        nomes_produtos = produto_input.split("+")
        produtos_db = Produto.query.filter(Produto.nomeProduto.in_(nomes_produtos)).all()
        aluno.produtos.extend(produtos_db)
        
    db.session.commit()
    print(f"Aluno {aluno.nomeAluno} atualizado com sucesso")
    return jsonify({"message": f"Aluno {aluno.nomeAluno} atualizado com sucesso"})


@admin_bp.route('/alunos/deletar/<int:id>', methods=["DELETE"])
def deletar_aluno(id:int) -> None:
    aluno = Aluno.query.get_or_404(id)
    
    db.session.delete(aluno)
    db.session.commit()
    
    print(f"Aluno {aluno.nomeAluno} removido com sucesso")
    return jsonify({"message": f"Aluno {aluno.nomeAluno} removido com sucesso"})


#################################################
##### Gerenciamento de Eventos no rota Admin.####
#################################################

@admin_bp.route("/eventos/listar", methods=["GET"])
def listar_eventos():
    eventos = PalestrasEventos.query.all()
    return render_template('listaEventos.html', eventos=eventos)


@admin_bp.route("/eventos/cadastrar", methods=["GET","POST"])
def cadastrar_evento():
    if "POST" == request.method:
        try:
            nome_evento = request.form.get('nomeEvento')
            data_inicial = request.form.get('dataInicial')
            hora_inicial = request.form.get('horaInicial')
            data_final = request.form.get('dataFinal')
            hora_final = request.form.get('horaFinal')
            nome_palestrante = request.form.get('nomePalestrante')
            
            data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
            data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
            
            novo_evento = PalestrasEventos(
                nomeEvento=nome_evento,
                dataInicial=data_inicial,
                dataFinal=data_final,
                nomePalestrate=nome_palestrante
            )
            print(f"Obj evento criado - {novo_evento}")
            db.session.add(novo_evento)
            db.session.commit()
            print(f"Adicioando ao Banco de Dados.")
            
            flash("Evento cadastrado com sucesso!", 'success')
            return redirect(url_for('admin.cadastrar_evento'))
        
        except Exception as e:
            db.session.rollback()
            print("Erro ao cadastrar evento:", e)
            flash(f"Erro ao cadastrar evento: {str(e)}", "error")
            return redirect(url_for('admin.cadastrar_evento'))
    
    return render_template("cadastroEventos.html")

@admin_bp.route("/eventos/editar/<int:id>", methods=["POST"])
def editar_evento(id:int) -> None:
    evento = PalestrasEventos.query.get_or_404(id)

    nome_evento = request.form.get('nomeEvento')
    data_inicial = request.form.get('dataInicial')
    data_final = request.form.get('dataFinal')
    nome_palestrante = request.form.get('nomePalestrante')

    if nome_evento:
        evento.nomeEvento = nome_evento
    if data_inicial:
        evento.dataInicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        evento.dataFinal = datetime.strptime(data_final, '%Y-%m-%d').date()
    if nome_palestrante:
        evento.nomePalestrante = nome_palestrante

    db.session.commit()
    flash("Evento atualizado com sucesso!", "success")
    return jsonify({"success": True, "message": "Evento atualizado!"})

@admin_bp.route("/eventos/deletar/<int:id>", methods=["DELETE"])
def deletar_evento(id:int) -> None:
    evento = PalestrasEventos.query.get_or_404(id)
    db.session.delete(evento)
    db.session.commit()
    return jsonify({"message": "Evento deletado com sucesso!"}), 200