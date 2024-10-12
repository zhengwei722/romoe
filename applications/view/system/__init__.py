from flask import Flask, Blueprint


from applications.view.system.index import bp as index_bp
from applications.view.system.log import bp as log_bp

from applications.view.system.monitor import bp as monitor_bp
from applications.view.system.passport import bp as passport_bp
from applications.view.system.power import bp as power_bp
from applications.view.system.rights import bp as right_bp
from applications.view.system.role import bp as role_bp
from applications.view.system.user import bp as user_bp

# 创建sys
system_bp = Blueprint('system', __name__, url_prefix='/system')


def register_system_bps(app: Flask):
    # 在admin_bp下注册子蓝图
    system_bp.register_blueprint(user_bp)
    system_bp.register_blueprint(monitor_bp)
    system_bp.register_blueprint(log_bp)
    system_bp.register_blueprint(power_bp)
    system_bp.register_blueprint(role_bp)

    system_bp.register_blueprint(passport_bp)
    system_bp.register_blueprint(right_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(system_bp)
