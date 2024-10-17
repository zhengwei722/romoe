import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from applications.extensions import db


class Knowledge(db.Model):
    __tablename__ = 'knowledge'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='ID')
    uid = db.Column(db.Integer)
    knowledgeName = db.Column(db.String(255), comment='知识库名字')
    knowledgeId = db.Column(db.String(255), comment='知识库ID')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')

