import datetime
from applications.extensions import db

class InviteRecord(db.Model):
    __tablename__ = 'invite_record'
    id = db.Column(db.Integer, primary_key=True)
    inviter_id = db.Column(db.Integer, comment='邀请者ID')
    invitee_id = db.Column(db.Integer, comment='受邀者ID')
    isreturnedCash = db.Column(db.Integer,default=0, comment='是否返现') # 0 未返现 1 已返现
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='最近更新时间')