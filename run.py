from flask import Flask, render_template
from app.routes import all_blueprints

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.secret_key = '57ee3757ba351d795da0b100ce3bfb97d623fb24d2ce123380a4d3ee21d1e076'

# Registra os blueprints
for bp in all_blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return render_template("welcome.html",)



if __name__ == "__main__":
    app.run(debug=True)
