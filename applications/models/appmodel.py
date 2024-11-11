import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from applications.extensions import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Appmodel(db.Model):
    __tablename__ = 'appmodel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    model_name = db.Column(db.String(99), comment='模型名称')
    model_id = db.Column(db.String(99), comment='模型ID')
    enable = db.Column(db.Integer, default=0, comment='启用')
    access_level = db.Column(db.Integer, default=0, comment='会员可用')
    ratio = db.Column(db.Float(precision=2), default=0.0, comment='倍率')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='最近更新时间')
    type = db.Column(db.Integer,  comment='模型类型') # 0:对话 1:画图

class Applist(db.Model):
    __tablename__ = 'applist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    app_name = db.Column(db.String(99), comment='应用名称')
    app_key = db.Column(db.String(99), comment='应用KEY')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='最近更新时间')

class Appmodelrole(db.Model):
    __tablename__ = 'appmodelrole'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    role_name = db.Column(db.String(99), comment='角色名称')
    role_prompt = db.Column(db.Text, comment='角色提示')
    role_icon = db.Column(db.String(256), comment='角色图标')
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