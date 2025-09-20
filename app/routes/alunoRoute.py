from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, Aluno

aluno_bp = Blueprint("aluno", __name__,url_prefix='/aluno')


@aluno_bp.route('/home', methods=["GET"])
def home_index_aluno():
    
    # Aqui fica a página principal com uma Navbar no centro dos produtos.
    return render_template("baseAlunos.html")






