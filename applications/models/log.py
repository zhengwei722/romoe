import datetime
from applications.extensions import db

class AdminLog(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(10))
    uid = db.Column(db.Integer)
    url = db.Column(db.String(255))
    request_body = db.Column(db.Text)
    response_body  = db.Column(db.Text)
    starttime = db.Column(db.String(255))
    endtime = db.Column(db.String(255))
    totaltime  = db.Column(db.String(255))
    success = db.Column(db.Integer)
    tips = db.Column(db.String(255))


'''
id
method
url
请求体（加密储存）
开始时间
结束时间
总耗时
返回数据（加密储存）
是否成功
操作人
tips
'''