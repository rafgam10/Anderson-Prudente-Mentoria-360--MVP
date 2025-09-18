from .loginRoute import login_bp
from .adminRoute import admin_bp

all_blueprints = [login_bp]
all_blueprints.append(admin_bp)