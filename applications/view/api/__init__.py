from flask import Flask, Blueprint
from applications.common.utils.http import CustomResponse ,CustomStatus
from applications.view.api.user import bp as user_bp
from applications.view.api.knowledge import bp as knowledge_bp
from applications.view.api.appmodel import bp as appmodel_bp
from applications.view.api.pay import bp as pay_bp
from applications.config import cfg

# 创建sys
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.get('/version')
def version():
    return CustomResponse(msg="查询成功",data={"welcome": "Romoe OpenAPI",'version': cfg['SYSTEM_VERSION']})


def register_api_bps(app: Flask):
    # 在admin_bp下注册子蓝图
    api_bp.register_blueprint(user_bp)
    api_bp.register_blueprint(knowledge_bp)
    api_bp.register_blueprint(appmodel_bp)
    api_bp.register_blueprint(pay_bp)
    app.register_blueprint(api_bp)

