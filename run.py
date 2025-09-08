from flask import Flask
from app.routes import all_blueprints

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.secret_key = 'mentoria360'

# Registra os blueprints
for bp in all_blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return "<h1>Home Mentoria 360° 🚀</h1>"

if __name__ == "__main__":
    app.run(debug=True)
