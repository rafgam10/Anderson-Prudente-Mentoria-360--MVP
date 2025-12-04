from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    jsonify,
    request,
    flash
)



mentoria_bp = Blueprint("mentoria", __name__, url_prefix="/mentorias")

## Rotas de Mentorias:

@mentoria_bp.route("/cadastrar-mentoria", methods=["GET", "POST"])
def cadastrar_mentorias():
    return render_template("telasAdmin/cadastroMentoria.html",)

@mentoria_bp.route("/listar-mentoria", methods=["GET"])
def listar_mentorias():
    return render_template("telasAdmin/listaMentoria.html",)
