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
from applications.models import Role
from applications.models import User, AdminLog ,Knowledge,Appmodel
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
import json
import requests
bp = Blueprint('appmodel', __name__, url_prefix='/appmodel')

@bp.get('/list')
@token_required_decorator
@log_decorator
def list(userId):
    try:
        user = User.query.filter_by(id=userId).first()
        if user.is_membership_expired():
            access_level = 0
        else:
            access_level = 1
        appmodel_list = Appmodel.query.filter_by(enable=1)
        data = [{
            'knowledgeName': appmodel.model_name,
            'knowledgeId': appmodel.model_id,
            'enable': (access_level == 1) or (access_level == 0 and appmodel.access_level == 0)
        } for appmodel in appmodel_list]
        return CustomResponse(msg="查询成功",data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))


