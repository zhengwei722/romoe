from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role
from applications.models import User, AdminLog ,Knowledge,Appmodel,Applist,Appmodelrole
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
bp = Blueprint('app', __name__, url_prefix='/app')

@bp.get('/modellist')
@log_decorator
def modellist():
    try:
        appmodel_list = Appmodel.query.filter_by(enable=1)
        data = [{
            'id':appmodel.id,
            'model_name': appmodel.model_name,
            'model_id': appmodel.model_id,
            'enable':appmodel.access_level == 0,
            'type':appmodel.type
        } for appmodel in appmodel_list]
        return CustomResponse(msg="查询成功",data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))


@bp.get('/applist')
@log_decorator
def applist():
    try:
        appmodel_list = Applist.query.all()
        data = [{
            'id':appmodel.id,
            'app_name': appmodel.app_name,
            'app_key': appmodel.app_key,
        } for appmodel in appmodel_list]
        return CustomResponse(msg="查询成功",data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))



@bp.get('/rolelist')
@log_decorator
def rolelist():
    try:
        appmodel_list = Appmodelrole.query.all()
        data = [{
            'id':appmodel.id,
            'role_name': appmodel.role_name,
            'role_prompt': appmodel.role_prompt,
            'role_icon': appmodel.role_icon,
        } for appmodel in appmodel_list]
        return CustomResponse(msg="查询成功",data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))