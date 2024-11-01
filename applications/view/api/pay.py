from itertools import product

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
from applications.models import User, AdminLog, Knowledge, Appmodel, PayOrder
from applications.common.utils.http import CustomResponse, CustomStatus
import random
from flask_mail import Message
from applications.extensions import db, flask_mail
from applications.config import cfg
from sqlalchemy.exc import SQLAlchemyError
from aiosmtplib.errors import SMTPDataError
from applications.common.utils.redis import conn_redis_pool
from applications.common.utils.jwt import token_required_decorator, create_jwt_token
from applications.common.utils.logger import log_decorator
import uuid
import json
import requests
from applications.common.utils.alipay import get_pay_url, verify_pay, changeUserIdentity, changeUserBalance, \
    generate_order_id

bp = Blueprint('pay', __name__, url_prefix='/pay')


@bp.post('alipay')
@token_required_decorator
@log_decorator
def get_alipay(userId):
    try:
        amount = request.json.get('amount')
        paytype = request.json.get('paytype')
        note = request.json.get('note')
        order = PayOrder(order_id=generate_order_id(), uid=userId, amount=float(amount), status=0, pay_method='支付宝',
                         pay_type=paytype, note=note)
        db.session.add(order)
        db.session.flush()
        order_id = order.order_id
        res = get_pay_url(order_id, float(amount), note)
        db.session.commit()
        return CustomResponse(msg="操作成功", data=res)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误", data=str(e))


@bp.post('verify_pay')
@log_decorator
def alipay_verify_pay():
    try:
        data = request.form.to_dict()
        signature = data.pop("sign")
        timestamp = data.get("gmt_payment")
        out_trade_no = request.form.get('out_trade_no')
        order = PayOrder.query.filter(PayOrder.order_id == out_trade_no).first()
        if order is None:
            return CustomResponse(msg="支付失败", data="订单不存在")
        if verify_pay(data, signature):
            order.status = 1
            order.pay_time = timestamp
            pay_note = order.note

            uid = order.uid
            user = User.query.filter(User.id == uid).first()
            role = Role.query.filter(Role.name == pay_note).first()
            user.add_diamonds(role.diamonds)
            user.add_words(role.words)
            user.extend_membership(role.member_day)
            default_role = [role.id]
            roles = Role.query.filter(Role.id.in_(default_role)).all()
            user.role = roles


            db.session.add(user)
            db.session.add(order)
            db.session.commit()
            return CustomResponse(msg="支付成功", data="支付成功")
        return CustomResponse(msg="支付失败", data="验证支付失败")

    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误", data=str(e))


@bp.get('orderlist')
@token_required_decorator
@log_decorator
def get_order_list(userId):
    try:
        pay_list = PayOrder.query.filter(PayOrder.uid == userId).all()
        data = [{
            'id': pay.id,
            'uid': pay.uid,
            'order_id': pay.order_id,
            'amount': pay.amount,
            'status': pay.status,
            'pay_method': pay.pay_method,
            'pay_type': pay.pay_type,
            'note': pay.note,
            'created_at': (pay.created_at).strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': (pay.updated_at).strftime('%Y-%m-%d %H:%M:%S'),
            'pay_time': (pay.pay_time).strftime('%Y-%m-%d %H:%M:%S') if pay.pay_time else None,
        } for pay in pay_list]
        return CustomResponse(msg="操作成功", data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误", data=str(e))


@bp.get('productlist')
@token_required_decorator
@log_decorator
def get_product_list(userId):
    try:
        user = User.query.filter(User.id == userId).first()
        if user.identity_type == '学生':
            products = Role.query.filter(Role.code == 'studentvip').all()
        else:
            products = Role.query.filter(Role.code == 'workervip').all()
        data = [{
            'id': product.id,
            'name': product.name,
            'code': product.code,
            'price': product.price,
            'member_day': product.member_day,
            'diamonds': product.diamonds,
            'words': product.words,

        } for product in products]
        return CustomResponse(msg="操作成功", data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误", data=str(e))