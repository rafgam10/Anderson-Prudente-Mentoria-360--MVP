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

mentoria_bp = Blueprint("mentoria", __name__, url_prefix="/mentorias")

## Rotas de Mentorias:

@mentoria_bp.route("/cadastrar-mentoria", methods=["GET", "POST"])
def cadastrar_mentorias():
    
    if request.method == "POST":

        nomeMentoria = request.form.get("nomeMentoria")
        entregaveis_raw = request.form.getlist("entregaveis[]")
        
        # transforma JSON → dict
        entregaveis = [json.loads(item) for item in entregaveis_raw]
        
        print("Nome:", nomeMentoria)
        print("Entregáveis:", entregaveis)
        
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
    
    return render_template("telasAdmin/cadastroMentoria.html")

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

    return render_template(
        "telasAdmin/listaMentoria.html", 
        lista_mentoria=lista_mentoria,
        entregaveis_count=entregaveis_count
    )


@mentoria_bp.route("/editar-mentoria/<int:id>", methods=["PUT"])
def editar_mentoria(id: int):
    data = request.get_json()
    novo_nome = data.get("nomeMentoria")

    mentoria = Mentoria.query.get(id)

    if not mentoria:
        return jsonify({"error": "Mentoria não encontrada"}), 404

    mentoria.nome = novo_nome
    db.session.commit()

    return jsonify({"message": "Mentoria atualizada com sucesso!"}), 200



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
