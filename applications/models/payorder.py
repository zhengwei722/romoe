import datetime
from applications.extensions import db

class PayOrder(db.Model):
    __tablename__ = 'payorder'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.String(64), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(16), nullable=False) # 0 未支付 1已支付 2已开票 4是失败
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    # 添加其他字段，如支付方式、支付时间等
    pay_method = db.Column(db.String(16), nullable=True)
    pay_time = db.Column(db.DateTime, nullable=True)
    # 添加其他字段，如支付方式、支付时间等
    pay_type = db.Column(db.Integer, nullable=True) # 0 会员类型 1 余额类型
    note = db.Column(db.String(256), nullable=True) # 商品标题