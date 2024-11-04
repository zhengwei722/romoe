from email.policy import default

from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc
from email_validator import validate_email, EmailNotValidError
from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role,InviteRecord
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
    user = User.query.filter_by(id=str(userId)).first()
    if user.is_membership_expired():
        default_role = ['2']
        roles = Role.query.filter(Role.id.in_(default_role)).all()
        user.role = roles
        user.words = 0
        db.session.commit()
        return CustomResponse(code=CustomStatus.MEMBERSHIP_EXPIRED.value, msg='会员已过期')
    return CustomResponse(code=CustomStatus.SUCCESS.value, msg='会员')


@bp.post('/diamonds')
@token_required_decorator
@log_decorator
def diamonds(userId):
    user = User.query.filter_by(id=str(userId)).first()
    if user.is_membership_expired():
        default_role = ['2']
        roles = Role.query.filter(Role.id.in_(default_role)).all()
        user.role = roles
        user.words = 0
        db.session.commit()
        return CustomResponse(code=CustomStatus.MEMBERSHIP_EXPIRED.value, msg='会员已过期')
    return CustomResponse(code=CustomStatus.SUCCESS.value, msg='会员')