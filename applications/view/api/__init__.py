from flask import Flask, Blueprint


from applications.view.api.user import bp as user_bp


# 创建sys
api_bp = Blueprint('api', __name__, url_prefix='/api')


def register_api_bps(app: Flask):
    # 在admin_bp下注册子蓝图
    api_bp.register_blueprint(user_bp)


    app.register_blueprint(api_bp)

