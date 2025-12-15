from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
    request
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import (
    db,
    Administrador,
    Aluno,
    Produto,
    PalestrasEventos,
    Fase,
    Atividade,
    Mentoria,
    Entregavel,
    Reuniao
)
from datetime import datetime

admin_bp = Blueprint("admin", __name__, url_prefix='/admin')


#### Página Admin Principal
@admin_bp.route('/home', methods=["GET"])
def index_admin():
    return render_template('telasAdmin/homeAdmin.html')

###########################################################
#### Gerenciamento de Administradores do Painel Admin.#####
###########################################################

@admin_bp.route('/admins/lista', methods=["GET"])
def lista_admins():
    array_admin = list(Administrador.query.all())
    return render_template('telasAdmin/listaAdmins.html', lista_admin=array_admin)

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
    return render_template('telasAdmin/cadastroAdmins.html')


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
        
    except Exception as e:
        db.session.rollback()
        
        

#################################################
##### Gerenciamento de Alunos no rota Admin.#####
#################################################

@admin_bp.route('/alunos/lista', methods=["GET"])
def lista_alunos():
    array_alunos = Aluno.query.all()
    return render_template('telasAdmin/listaAlunos.html', array_alunos=array_alunos)


@admin_bp.route('/alunos/cadastro', methods=["GET","POST"])
def cadastro_aluno():
    if request.method == "POST":
        
        inputNomeAluno = request.form.get('nomeAluno')
        inputEmailAluno = request.form.get('emailAluno')
        inputSenhaAluno = request.form.get('senhaAluno')
        inputCPFAluno = request.form.get('cpfAluno')
        
        mentoria_select = request.form.getlist('select_mentoria')
        
        # Exibir dados coletados.
        print("Nome:", inputNomeAluno)
        print("Email:", inputEmailAluno)
        print("Senha:", inputSenhaAluno)
        print("CPF:", inputCPFAluno)
        print("Mentoria selecionados:", mentoria_select)
        
        # Inserir alunos no DB:
        novo_aluno = Aluno(
            nomeAluno=inputNomeAluno,
            emailAluno=inputEmailAluno,
            senhaAluno=generate_password_hash(inputSenhaAluno),
            CPFAluno=inputCPFAluno
        )
            
        # Busca os produtos selecionado no DB:
        if mentoria_select:
            mentorias_db = Mentoria.query.filter(
                Mentoria.id.in_(mentoria_select)
            ).all()
            
            novo_aluno.mentorias.extend(mentorias_db)
            print("Mentorias associadas:", mentorias_db)
        
        db.session.add(novo_aluno)
        db.session.commit()
        print("Registro inserido no Banco de dados...")
        
        flash(f"Aluno {inputNomeAluno} cadastrado com sucesso!", "success")
        return redirect(url_for('admin.cadastro_aluno'))
    
    mentorias = db.session.query(Mentoria).all()
    return render_template('telasAdmin/cadastroAlunos.html', mentorias=mentorias)


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

@admin_bp.route('/entregaveis/<int:id>', methods=['PATCH'])
def atualizar_entregavel(id):
    entregavel = Entregavel.query.get_or_404(id)
    data = request.get_json()

    entregavel.status = data.get('status')

    if data.get('data_entrega'):
        entregavel.data_entrega = datetime.strptime(
            data.get('data_entrega'), '%Y-%m-%d'
        )
    else:
        entregavel.data_entrega = None

    db.session.commit()

    return jsonify({"success": True})



@admin_bp.route('/alunos/<int:aluno_id>/entregaveis')
def entregaveis_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)

    entregaveis = [
        {
            "id": e.id,
            "nome": e.nome,
            "status": e.status,
            "data_entrega": e.data_entrega.strftime('%d/%m/%Y') if e.data_entrega else None,
            "mentoria": e.mentoria.nome,
            "mentoria_id": e.mentoria.id
        }
        for e in aluno.entregaveis
    ]

    return {"entregaveis": entregaveis}


@admin_bp.route("/reuniao/add", methods=["POST"])
def criar_reuniao():
    data = request.get_json()

    aluno_id = data.get("aluno_id")
    mentoria_id = data.get("mentoria_id")
    data_reuniao = data.get("data_reuniao")

    if not all([aluno_id, mentoria_id, data_reuniao]):
        return jsonify({"error": "Dados incompletos"}), 400

    nova_reuniao = Reuniao(
        nome="Reunião",
        data=datetime.strptime(data_reuniao, "%Y-%m-%d"),
        id_aluno=aluno_id,
        id_mentoria=mentoria_id
    )

    db.session.add(nova_reuniao)
    db.session.commit()

    return jsonify({"success": True})

#################################################
##### Gerenciamento de Eventos no rota Admin.####
#################################################

@admin_bp.route("/eventos/listar", methods=["GET"])
def listar_eventos():
    eventos = PalestrasEventos.query.all()
    return render_template('telasAdmin/listaEventos.html', eventos=eventos)


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
                horaInicial=hora_inicial,
                dataFinal=data_final,
                horaFinal=hora_final,
                nomePalestrante=nome_palestrante
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
    
    return render_template("telasAdmin/cadastroEventos.html")

@admin_bp.route("/eventos/editar/<int:id>", methods=["POST"])
def editar_evento(id:int) -> None:
    evento = PalestrasEventos.query.get_or_404(id)

    nome_evento = request.form.get('nomeEvento')
    data_inicial = request.form.get('dataInicial')
    hora_inicial = request.form.get('horaInicial')
    data_final = request.form.get('dataFinal')
    hora_final = request.form.get('horaFinal')
    nome_palestrante = request.form.get('nomePalestrante')

    if nome_evento:
        evento.nomeEvento = nome_evento
    if data_inicial:
        evento.dataInicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if hora_inicial:
        evento.horaInicial = hora_inicial
    if data_final:
        evento.dataFinal = datetime.strptime(data_final, '%Y-%m-%d').date()
    if hora_inicial:
        evento.horaFinal = hora_final
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


#################################################
### Gerenciamento de Atividades no rota Admin.###
#################################################

@admin_bp.route("/atividades/listar", methods=["GET"])
def listar_atividades():
    atividades = Atividade.query.all()
    fases = Fase.query.all()
    return render_template('telasAdmin/listaAtividades.html', atividades=atividades, fases=fases)


@admin_bp.route("/atividades/cadastrar", methods=["GET", "POST"])
def cadastrar_atividades():
    if request.method == "POST":
        try:
            nome = request.form.get("nomeAtividade")
            descricao = request.form.get("descricaoAtividade")
            data_str = request.form.get("dataAtividade")
            hora_str = request.form.get("horaAtividade")
            plataforma = request.form.get("plataformaAtividade")
            fase_id_str = request.form.get("faseAtividade")

            if not fase_id_str:
                flash("Selecione uma fase antes de cadastrar.", "error")
                return redirect(url_for("admin.cadastrar_atividades"))

            fase_id = int(fase_id_str)


            # Conversão de data e hora
            data = datetime.strptime(data_str, "%Y-%m-%d").date()
            hora = datetime.strptime(hora_str, "%H:%M").time()

            nova_atividade = Atividade(
                nome_atividade=nome,
                descricao=descricao,
                data=data,
                hora=hora,
                plataforma=plataforma,
                fase_id=int(fase_id)
            )

            db.session.add(nova_atividade)
            db.session.commit()
            flash("Atividade cadastrada com sucesso!", "success")
            return redirect(url_for("admin.cadastrar_atividades"))
        
        except Exception as e:
            db.session.rollback()
            print("Erro ao cadastrar atividade:", e)
            flash(f"Erro ao cadastrar atividade: {e}", "error")
            return redirect(url_for("admin.cadastrar_atividades"))

    # GET - para preencher o select de fases dinamicamente
    fases = Fase.query.all()
    print(f"{fases}")
    return render_template("telasAdmin/cadastroAtividade.html", fases=fases)

@admin_bp.route("/atividades/editar/<int:id>", methods=["POST"])
def editar_atividade(id: int):
    atividade = Atividade.query.get_or_404(id)

    data = request.get_json()

    nome_atividade = data.get('nomeAtividade')
    descricao_atividade = data.get('descricaoAtividade')
    data_atividade = data.get('dataAtividade')
    hora_atividade = data.get('horaAtividade')
    plataforma = data.get('tipoAtividade')
    fase_id = data.get('faseAtividade')
    programa = data.get('programaAtividade')

    if nome_atividade:
        atividade.nome_atividade = nome_atividade
    if descricao_atividade:
        atividade.descricao = descricao_atividade
    if data_atividade:
        atividade.data = datetime.strptime(data_atividade, '%Y-%m-%d').date()
    if hora_atividade:
        atividade.hora = datetime.strptime(hora_atividade, '%H:%M').time()  # ✅ formato corrigido
    if plataforma:
        atividade.plataforma = plataforma
    if fase_id:
        atividade.fase_id = int(fase_id)
    if programa:
        atividade.plataforma = programa  # ou outro campo correto para 'programa'

    db.session.commit()
    flash("Atividade atualizada com sucesso!", "success")
    return jsonify({"success": True, "message": "Atividade atualizada!"})


# -------------------------------
# DELETAR ATIVIDADE
# -------------------------------
@admin_bp.route("/atividades/deletar/<int:id>", methods=["DELETE"])
def deletar_atividade(id: int):
    atividade = Atividade.query.get_or_404(id)
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"message": "Atividade deletada com sucesso!"}), 200