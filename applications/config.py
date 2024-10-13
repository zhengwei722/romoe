import logging
from datetime import timedelta
import redis
import toml
import os
# from urllib.parse import quote_plus as urlquote

cfg = None
env_filenames = [
    os.getenv("CUSTOM_ENV_TOML") or 'pro_env.yaml',
    'test_env.yaml',
    'local_env.yaml'
]

for env_filename in env_filenames:
    try:
        with open(env_filename, encoding='utf-8') as tomlfile:
            cfg = toml.load(tomlfile)
        print(f"环境配置文件加载成功。当前环境： {env_filename}")
        break  # 如果文件存在并成功加载，则跳出循环
    except FileNotFoundError:
        print(f"环境文件 {env_filename} 未找到。尝试下一个文件...")
        cfg = None  # 重置 cfg 以确保在下一个循环中不会使用旧的配置


class BaseConfig:
    SUPERADMIN = cfg['SUPERADMIN']

    SYSTEM_NAME = cfg['SYSTEM_NAME']
    # 主题面板的链接列表配置
    SYSTEM_PANEL_LINKS = [
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "官方网站",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开发文档",
            "href": "http://www.pearadmin.com"
        },
        {
            "icon": "layui-icon layui-icon-auz",
            "title": "开源地址",
            "href": "https://gitee.com/Jmysy/Pear-Admin-Layui"
        }
    ]

    UPLOADED_PHOTOS_DEST = cfg['UPLOADED_PHOTOS_DEST']
    UPLOADED_FILES_ALLOW = ['gif', 'jpg']
    UPLOADS_AUTOSERVE = True

    # JSON配置
    JSON_AS_ASCII = False

    SECRET_KEY = cfg['SECRET_KEY']

    # redis配置
    REDIS_HOST = cfg['REDIS_HOST']
    REDIS_PORT = cfg['REDIS_PORT']
    REDIS_PASSWORD = cfg['REDIS_PASSWORD']

    # mysql 配置
    MYSQL_USERNAME = cfg['MYSQL_USERNAME']
    MYSQL_PASSWORD = cfg['MYSQL_PASSWORD']
    MYSQL_HOST = cfg['MYSQL_HOST']
    MYSQL_PORT = cfg['MYSQL_PORT']
    MYSQL_DATABASE = cfg['MYSQL_DATABASE']

    # mysql 数据库的配置信息
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

    # 默认日志等级
    LOG_LEVEL = logging.WARN
    """
    flask-mail配置
    """
    MAIL_SERVER = cfg['MAIL_SERVER']
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_PORT = cfg['MAIL_PORT']
    MAIL_USERNAME = cfg['MAIL_USERNAME']
    MAIL_PASSWORD = cfg['MAIL_PASSWORD']  # 生成的授权码
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    """
    session
    """
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    SESSION_TYPE = cfg['SESSION_TYPE'] # 默认使用文件系统来保存会话
    SESSION_PERMANENT = False  # 会话是否持久化
    SESSION_USE_SIGNER = True  # 是否对发送到浏览器上 session 的 cookie 值进行加密
    SESSION_REDIS_DB = cfg['REDIS_DB']
    SESSION_REDIS = redis.from_url(f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{SESSION_REDIS_DB}')

