import datetime
from applications.extensions import db


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, comment='角色ID')
    name = db.Column(db.String(255), comment='角色名称')
    code = db.Column(db.String(255), comment='角色标识')
    enable = db.Column(db.Integer, comment='是否启用')
    member_day = db.Column(db.Integer, comment='天数')
    diamonds = db.Column(db.Integer, comment='钻石')
    words = db.Column(db.Integer, comment='文字')
    sort = db.Column(db.Integer, comment='排序')
    price = db.Column(db.Float(precision=2), default=0.0, comment='价格')
    cashback = db.Column(db.Float(precision=2), default=0.0, comment='返现')
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')

