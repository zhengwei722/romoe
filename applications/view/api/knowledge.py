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
from applications.models import User, AdminLog ,Knowledge
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
bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


@bp.post('/create')
@token_required_decorator
@log_decorator
def create(userId):
    try:
        knowledgeName = request.json.get('knowledgeName')
        if knowledgeName is None:
            return CustomResponse(code=CustomStatus.INVALID_PARAMETER.value, msg="请填写知识库名字")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整",data=str(e))

    try:
        knowledge = Knowledge.query.filter_by(knowledgeName=knowledgeName).first()
        if knowledge:
            return CustomResponse(code=CustomStatus.USERNAME_ALREADY_EXISTS.value, msg="知识库名称重复")
        knowledge_count = Knowledge.query.filter_by(uid=userId).count()

        if knowledge_count >=cfg['DIFY_DATESET_MAX']:
            return CustomResponse(code=CustomStatus.MAXIMUM_NUMBER_OF_COLLECTIONS_REACHED.value, msg="知识库数量以达到最大值")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))

    try:
        payload = json.dumps({"name": knowledgeName, "permission": "only_me"})
        key = cfg['DIFY_DATASET_KEY']
        headers = {
             'Authorization': f'Bearer {key}',
             'Content-Type': 'application/json'
          }
        url = cfg['DIFY_URL']+'/datasets'
        response = requests.request("POST", url, headers=headers, data=payload)

        knowledgeId = response.json()['id']

        knowledge = Knowledge(knowledgeName=knowledgeName, knowledgeId=knowledgeId,uid = userId)
        db.session.add(knowledge)
        db.session.commit()
        return CustomResponse(msg="创建成功")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))

@bp.get('/list')
@token_required_decorator
@log_decorator
def list(userId):
    try:
        knowledge_list = Knowledge.query.filter_by(uid=userId).all()
        data=[{
                'id': knowledge.id,
                'knowledgeName': knowledge.knowledgeName,
                'knowledgeId': knowledge.knowledgeId,
                'create_at': (knowledge.create_at).strftime('%Y-%m-%d %H:%M:%S')
            } for knowledge in knowledge_list]
        return CustomResponse(msg="获取成功",data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))


@bp.delete('/delete')
@token_required_decorator
@log_decorator
def delete(userId):
    try:
        knowledgeId = request.json.get('knowledgeId')
        if knowledgeId is None:
            return CustomResponse(code=CustomStatus.INVALID_PARAMETER.value, msg="请填写知识库ID")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整", data=str(e))

    try:
        knowledge = Knowledge.query.filter_by(knowledgeId=knowledgeId).first()
        if not knowledge:
            return CustomResponse(code=CustomStatus.USERNAME_ALREADY_EXISTS.value, msg="知识库不存在")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))

    try:

        key = cfg['DIFY_DATASET_KEY']
        headers = {
             'Authorization': f'Bearer {key}',
          }
        url = cfg['DIFY_URL']+'/datasets/'+str(knowledgeId)
        response = requests.request("DELETE", url, headers=headers)
        #
        if response.status_code != 200:
            return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误")
        res = Knowledge.query.filter_by(knowledgeId=knowledgeId).delete()
        db.session.commit()

        return CustomResponse(msg="删除成功")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))