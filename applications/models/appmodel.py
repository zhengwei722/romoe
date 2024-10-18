import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from applications.extensions import db


class Appmodel(db.Model):
    __tablename__ = 'appmodel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    model_name = db.Column(db.String(99), comment='模型名称')
    model_id = db.Column(db.String(99), comment='模型ID')
    enable = db.Column(db.Integer, default=0, comment='启用')
    access_level = db.Column(db.Integer, default=0, comment='访问限制')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='最近更新时间')

'''
id
username
nickname
password_hash
role
enable
create_at
update_at
'''