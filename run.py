from flask import Flask, render_template
from app.routes import all_blueprints
from flask_login import LoginManager
from app.models import db, Administrador, Aluno

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.secret_key = '57ee3757ba351d795da0b100ce3bfb97d623fb24d2ce123380a4d3ee21d1e076'
app.config.from_object('app.config')

db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login_page'



@login_manager.user_loader
def load_user(user_id):
    user = Administrador.query.get(int(user_id))
    if user:
        return user
    return Aluno.query.get(int(user_id))


# Registra os blueprints
for bp in all_blueprints:
    app.register_blueprint(bp)

from app.models import *

@app.route("/")
def index():
    return render_template("welcome.html",)



if __name__ == "__main__":
    app.run(debug=True)
