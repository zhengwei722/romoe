from email.policy import default

from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc
from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role, InviteRecord, Appmodel
from applications.models import User, AdminLog
from applications.common.utils.http import CustomResponse ,CustomStatus
import random
from flask_mail import Message
from applications.extensions import db, flask_mail
from applications.config import cfg
from sqlalchemy.exc import SQLAlchemyError
from aiosmtplib.errors import SMTPDataError
from applications.common.utils.redis import conn_redis_pool
from applications.common.utils.jwt import token_required_decorator,create_jwt_token
from applications.common.utils.logger import log_decorator
import uuid
import pytz



bp = Blueprint('chat', __name__, url_prefix='/chat')


@bp.post('/words')
@token_required_decorator
@log_decorator
def words(userId):
    quantity = request.json.get('quantity')
    modelid = request.json.get('modelid')
    quantity = int(quantity)
    user = User.query.filter_by(id=userId).first()
    model = Appmodel.query.filter_by(id=modelid).first()
    if not user or not model:
        return CustomResponse(code=CustomStatus.USER_NOT_FOUND.value, msg='用户或模型不存在')
    if quantity > 0:
        return CustomResponse(code=CustomStatus.INSUFFICIENT_AUTHORITY.value, msg='权限不足')
    if user.words == 0 :
        return CustomResponse(code=CustomStatus.INSUFFICIENT_BALANCE.value, msg='余额不足')
    quantity *=model.ratio
    quantity = int(quantity)
    user.add_words(quantity)
    db.session.commit()
    return CustomResponse(msg='扣减成功')



@bp.post('/diamonds')
@token_required_decorator
@log_decorator
def diamonds(userId):
    user = User.query.filter_by(id=str(userId)).first()
    if not user:
        return CustomResponse(code=CustomStatus.USER_NOT_FOUND.value, msg='用户不存在')
    user.add_diamonds(1)
    db.session.commit()
    return CustomResponse(msg='增加成功')
