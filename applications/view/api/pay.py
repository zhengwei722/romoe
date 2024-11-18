from datetime import datetime
from itertools import product

from flask import Blueprint, session, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role,PayOrder,InviteRecord,WithdrawRecord
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
        id = request.json.get('id')
        role = Role.query.filter(Role.id == id).first()
        user = User.query.filter(User.id == userId).first()
        if user.is_membership_expired():
            identitystatus = 0
        else:
            identitystatus = 1

        order = PayOrder(order_id=generate_order_id(), uid=userId, price=role.price, status=0, pay_method='支付宝',
                         pay_type=0, note=role.name,identitystatus=identitystatus )
        db.session.add(order)
        db.session.flush()
        order_id = order.order_id
        res = get_pay_url(order_id, role.price, role.name)
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
            # 改变用户余额状态
            user.add_diamonds(role.diamonds)
            user.add_words(role.words)
            user.extend_membership(role.member_day)
            # 改变用户身份
            default_role = [role.id]
            roles = Role.query.filter(Role.id.in_(default_role)).all()
            user.role = roles

            # 反佣金
            inviteRecord = InviteRecord.query.filter(InviteRecord.invitee_id == uid).first()
            if inviteRecord and inviteRecord.isreturnedCash == 0:
                inviter = User.query.filter(User.id == inviteRecord.inviter_id).first()
                if order.note == '月度会员':
                    inviter.add_commission(10)
                    inviteRecord.isreturnedCash = 1
                    db.session.add(inviteRecord)
                if order.note == '年度会员':
                    inviter.add_commission(50)
                    inviteRecord.isreturnedCash = 1
                    db.session.add(inviteRecord)

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
            'price': pay.price,
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
        packet = PayOrder.query.filter(PayOrder.uid == userId and PayOrder.status == 1 and  PayOrder.identitystatus ==0 and PayOrder.note == '流量包').first()
        products = Role.query.filter(Role.sort == '3').all()
        # packet_exists = packet is not None
        data = [{
            'id': product.id,
            'name': product.name,
            'code': product.code,
            'price': product.price,
            'member_day': product.member_day,
            'diamonds': product.diamonds,
            'words': product.words,
            'status': False if packet  and product.code == 'packet' and [role.id for role in user.role][0] ==2 else True,
        } for product in products]
        return CustomResponse(msg="操作成功", data=data)
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误", data=str(e))


@bp.post('withdraw')
@token_required_decorator
@log_decorator
def withdraw(userId):
    try:
        amount = request.json.get('amount')
        user = User.query.filter(User.id == userId).first()
        if not user.alipay_account or not user.alipay_name:
            return CustomResponse(code=CustomStatus.INVALID_PARAMETER.value, msg="请先完善支付宝信息")
        if float(amount) > user.commission:
            return CustomResponse(code=CustomStatus.INSUFFICIENT_BALANCE.value, msg="余额不足")

        withdraw = WithdrawRecord(amount=float(amount), user_id=userId, account=user.alipay_account, name=user.alipay_name)
        # 扣除用户余额
        user.commission -= float(amount)
        db.session.add(withdraw)
        db.session.commit()
        return CustomResponse(msg="操作成功")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误", data=str(e))