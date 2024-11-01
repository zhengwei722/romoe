import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from applications.extensions import db
from sqlalchemy import  Enum


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(20), comment='用户名')
    realname = db.Column(db.String(20), comment='真实名字')
    avatar = db.Column(db.String(255), comment='头像', default="/static/system/admin/images/avatar.jpg")
    password_hash = db.Column(db.String(128), comment='哈希密码')
    enable = db.Column(db.Integer, default=0, comment='启用')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='最近更新时间')
    diamonds = db.Column(db.Integer, comment='钻石',default=0)
    words = db.Column(db.Integer, comment='文字',default=10000)
    membershipExpirationDate = db.Column(db.DateTime,default=datetime.datetime.now, comment='会员到期时间')
    role = db.relationship('Role', secondary="user_role", backref=db.backref('user'), lazy='dynamic')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_membership_expired(self):
        """
        判断会员是否已过期。

        :return: 如果会员已过期返回True，否则返回False。
        """
        return self.membershipExpirationDate < datetime.datetime.now()

    def add_diamonds(self, amount):
        """
        增加或减少用户的钻石数量。

        :param amount: 要增加或减少的钻石数量，可以是正数或负数。
        """
        if not isinstance(amount, int):
            raise TypeError("增加或减少的钻石数量必须是一个整数。")

        self.diamonds += amount
        # 确保钻石数量不会变成负数
        if self.diamonds < 0:
            self.diamonds = 0
        db.session.add(self)
        db.session.commit()
        return self.diamonds

    def add_words(self, amount):
        """
        增加或减少用户的钻石数量。

        :param amount: 要增加或减少的钻石数量，可以是正数或负数。
        """
        if not isinstance(amount, int):
            raise TypeError("增加或减少的文字数量必须是一个整数。")

        self.words += amount
        # 确保钻石数量不会变成负数
        if self.words < 0:
            self.words = 0
        db.session.add(self)
        db.session.commit()
        return self.words

    def extend_membership(self,days):
        """
        将会员到期时间增加天。
        """
        if days == 0:
            # 如果传入的天数为0，则设置会员到期时间为2099年12月31日
            new_expiration_date = datetime.datetime(2099, 12, 31)
        else:
            # 获取当前会员到期时间
            current_expiration_date = self.membershipExpirationDate
            new_expiration_date = current_expiration_date + datetime.timedelta(days=days)
        # 更新会员到期时间
        self.membershipExpirationDate = new_expiration_date
        # 保存更新
        db.session.add(self)
        db.session.commit()
        # 返回新的会员到期时间
        return self.membershipExpirationDate
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