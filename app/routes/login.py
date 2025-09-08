from flask import (
    Blueprint,
    render_template,
    request
)
from flask_login import (
    login_required,
    logout_user
)

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["GET"])
def login():
    print("blueprint login deu certo")
    return render_template('login.html')

@login_bp.route('/login', methods=["POST"])
def login_acesso():
    if request.method == "post":
        pass