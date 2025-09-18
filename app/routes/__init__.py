from .loginRoute import login_bp
from .adminRoute import admin_bp
from .alunoRoute import aluno_bp

all_blueprints = [login_bp]
all_blueprints.append(admin_bp)
all_blueprints.append(aluno_bp)