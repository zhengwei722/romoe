from applications.view.system import register_system_bps
from applications.view.api import register_api_bps

def init_bps(app):
    register_system_bps(app)
    register_api_bps(app)

