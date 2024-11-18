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

class WithdrawRecord(db.Model):
    __tablename__ = 'withdraw_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, comment='用户ID')
    amount = db.Column(db.Float, comment='提现金额')
    account = db.Column(db.String(255), comment='提现账号')
    name = db.Column(db.String(255), comment='提现姓名')
    status = db.Column(db.Integer, default=0, comment='提现状态') # 0 未处理 1 已处理
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='最近更新时间')