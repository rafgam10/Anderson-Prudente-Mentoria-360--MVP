from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    jsonify,
    request,
    flash
)
import json, datetime


# Import Models
from app.models import db
from app.models.Mentoria_model import Mentoria
from app.models.Entregavel_model import Entregavel
from app.models.EntregavelModelo import EntregavelModelo

mentoria_bp = Blueprint("mentoria", __name__, url_prefix="/mentorias")

## Rotas de Mentorias:

@mentoria_bp.route("/cadastrar-mentoria", methods=["GET", "POST"])
def cadastrar_mentorias():
    
    if request.method == "POST":

        nomeMentoria = request.form.get("nomeMentoria")
        entregaveis_raw = request.form.getlist("entregaveis[]")
        
        # transforma JSON → dict
        entregaveis = [json.loads(item) for item in entregaveis_raw]
        
        # Verifica duplicado
        existente = Mentoria.query.filter_by(nome=nomeMentoria).first()
        if existente:
            flash(f"Já existe uma mentoria com o nome '{nomeMentoria}'!", "danger")
            return redirect(url_for("mentoria.cadastrar_mentorias"))

        data_criacao_mentoria = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # cria mentoria
        obj_mentoria = Mentoria(nomeMentoria, None, data_criacao_mentoria)
        db.session.add(obj_mentoria)
        db.session.commit()  # agora o obj_mentoria.id existe
        
        # pega ID sem precisar buscar no BD
        id_mentoria = obj_mentoria.id
        
        # cria os entregáveis
        for entregar in entregaveis:
            obj_entregar = Entregavel(
                id_mentoria=id_mentoria,
                nome=entregar.get("nome")
            )
            db.session.add(obj_entregar)

        db.session.commit()  # commit único

        flash("Mentoria criada com sucesso!", "success")
        return redirect(url_for("mentoria.cadastrar_mentorias"))
    
    modelos = EntregavelModelo.query.order_by(EntregavelModelo.nome).all()
    return render_template("telasAdmin/cadastroMentoria.html", modelos=modelos)

@mentoria_bp.route("/modelo/add", methods=["POST"])
def add_modelo():
    data = request.get_json()
    nome = data.get("nome")
    if not nome:
        return jsonify({"error": "Nome é obrigatório"}), 400
    
    # Verifica duplicado
    existente = EntregavelModelo.query.filter_by(nome=nome).first()
    if existente:
        return jsonify({"error": "Já existe um modelo com este nome"}), 400
    
    novo = EntregavelModelo(nome=nome)
    db.session.add(novo)
    db.session.commit()
    
    return jsonify({"id": novo.id, "nome": novo.nome}), 201

@mentoria_bp.route("/modelo/delete/<int:id>", methods=["DELETE"])
def delete_modelo(id):
    modelo = EntregavelModelo.query.get_or_404(id)
    db.session.delete(modelo)
    db.session.commit()
    return jsonify({"message": "Modelo removido com sucesso"}), 200

@mentoria_bp.route("/verificar-nome", methods=["POST"])
def verificar_nome():
    data = request.get_json()
    nome = data.get("nome")
    if not nome:
        return jsonify({"existe": False})
    
    existente = Mentoria.query.filter_by(nome=nome).first()
    return jsonify({"existe": existente is not None})

@mentoria_bp.route("/listar-mentoria", methods=["GET"])
def listar_mentorias():

    lista_mentoria = db.session.query(Mentoria).all()

    # cria um dicionário com total de entregáveis por mentoria
    entregaveis_count = {
        mentoria.id: db.session.query(Entregavel)
                               .filter_by(id_mentoria=mentoria.id)
                               .count()
        for mentoria in lista_mentoria
    }

    modelos = EntregavelModelo.query.order_by(EntregavelModelo.nome).all()
    
    return render_template(
        "telasAdmin/listaMentoria.html", 
        lista_mentoria=lista_mentoria,
        entregaveis_count=entregaveis_count,
        modelos=modelos
    )


@mentoria_bp.route("/editar-mentoria/<int:id>", methods=["PUT"])
def editar_mentoria(id: int):
    from app.models.Aluno import Aluno
    from app.models.AlunoEntregavel import AlunoEntregavel
    
    data = request.get_json()
    novo_nome = data.get("nomeMentoria")
    entregaveis_nomes = data.get("entregaveis", []) # Lista de nomes (strings)

    mentoria = Mentoria.query.get(id)
    if not mentoria:
        return jsonify({"error": "Mentoria não encontrada"}), 404

    # Atualiza nome
    mentoria.nome = novo_nome
    
    # Gerencia entregáveis
    atuais_nomes = [e.nome for e in mentoria.entregaveis]
    
    # 1. Remover entregáveis que não estão mais na lista nova
    for e in list(mentoria.entregaveis):
        if e.nome not in entregaveis_nomes:
            # Remover instâncias deste entregável para todos os alunos
            AlunoEntregavel.query.filter_by(entregavel_id=e.id).delete()
            db.session.delete(e)
            
    # 2. Adicionar novos entregáveis
    for nome in entregaveis_nomes:
        if nome not in atuais_nomes:
            novo_e = Entregavel(id_mentoria=id, nome=nome)
            db.session.add(novo_e)
            db.session.flush() # Garante que o ID do novo_e seja gerado
            
            # Criar instância para todos os alunos vinculados a esta mentoria
            for aluno in mentoria.alunos:
                nova_instancia = AlunoEntregavel(
                    aluno=aluno,
                    entregavel_id=novo_e.id,
                    status='Pendente'
                )
                db.session.add(nova_instancia)

    db.session.commit()
    return jsonify({"message": "Mentoria atualizada com sucesso!"}), 200

@mentoria_bp.route("/entregaveis/<int:id>", methods=["GET"])
def get_entregaveis_mentoria(id):
    mentoria = Mentoria.query.get_or_404(id)
    res = [{"id": e.id, "nome": e.nome} for e in mentoria.entregaveis]
    return jsonify({"entregaveis": res})



@mentoria_bp.route("/deletar-mentoria/<int:id>", methods=["DELETE"])
def deletar_mentoria(id: int):
    mentoria = Mentoria.query.get(id)

    if not mentoria:
        return jsonify({"error": "Mentoria não encontrada"}), 404

    db.session.delete(mentoria)
    db.session.commit()

    return jsonify({
        "message": "Mentoria deletada com sucesso!",
        "id": id
    }), 200
