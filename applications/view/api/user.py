import time
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
from applications.common.utils.validate import verify_email



bp = Blueprint('user', __name__, url_prefix='/user')

'''
获取验证码接口
email:邮箱
'''
@bp.post('/get_email_code')
@log_decorator
def get_email_code():
    # 验证数据
    try:
        email = request.json.get('email')
        if email is None:
            return CustomResponse(code=CustomStatus.PARAM_ERROR.value, msg="请填写邮箱地址")
        # 验证email是否合法的email格式，是否有填写
        if not verify_email(email):
            return CustomResponse(code=CustomStatus.EMAIL_FORMAT_MISALIGNMENT.value, msg="邮箱格式错误")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整",data=str(e))
    # 发送验证码
    try:
        email_code = f"{random.randint(0, 999999):06d}"
        # 创建 Redis 连接
        redis_client = conn_redis_pool()
        redis_client.hset(f'email_code:{email}', mapping={'code': email_code, 'counter': 0})
        redis_client.expire(f'email_code:{email}', 300)  # 设置验证码有效期为5分钟


        body_content = cfg["LOGIN_CODE_EMAIL_BODY_CONTENT"].format(login_code=email_code)

        # msg = Message(subject="欢迎使用Romoe", recipients=email.split(";"), body=body_content)
        # flask_mail.send(msg)
        return CustomResponse(msg="发送成功")
    except SQLAlchemyError:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str('SQLAlchemyError'))
    except SMTPDataError:
        return CustomResponse(code=CustomStatus.OPERATE_DUPLICATE.value, msg="短时间内发送邮件次数过多，请稍后再试",data=str('SMTPDataError'))
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))


'''
注册接口-重置密码
email:邮箱
email_code:验证码
password:密码
confirm_password:确认密码
'''
@bp.post('/register')
@log_decorator
def register():
    # 验证数据
    try:
        email = request.json.get('email')
        email_code = request.json.get('verificationCode')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
        invite_code = request.json.get('invite_code')
        # identity_type = request.json.get('identity_type')
        if email is None:
            return CustomResponse(code=CustomStatus.PARAM_ERROR.value,msg="请填写邮箱地址")
        if password != confirm_password:
            return CustomResponse(code=CustomStatus.TWO_PASSWORDS_INCORRECT.value,msg="两次密码不一致")
        if email_code is None:
            return CustomResponse(code=CustomStatus.LOGIN_CODE_MISS.value,msg="请填写验证码")
        # if identity_type not in ["学生", "上班族"]:
        #     return CustomResponse(code=CustomStatus.INVALID_PARAMETER.value,msg="请选择用户类型")
        if not verify_email(email):
            return CustomResponse(code=CustomStatus.EMAIL_FORMAT_MISALIGNMENT.value, msg="邮箱格式错误")
        if len(password) < 8:
            return CustomResponse(code=CustomStatus.PASSWORD_INSUFFICIENT_LENGTH.value, msg="密码长度必须至少为8个字符")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整",data=str(e))
    # 验证码
    try:
        redis_client = conn_redis_pool()
        login_code_info = redis_client.hgetall(f'email_code:{email}')


        if login_code_info is None or len(login_code_info) == 0:
            return CustomResponse(code=CustomStatus.LOGIN_CODE_MISS.value, msg="未找到注册验证码或已过期")
        if login_code_info["code"] != email_code:
            counter =int(login_code_info["counter"])
            counter+=1
            if  counter >= int(cfg["LOGIN_CODE_MAX_TRY"]):
                redis_client.delete(f'email_code:{email}')
                return CustomResponse(code=CustomStatus.LOGIN_CODE_TO_MANY_TRY.value,msg="连续输入错误次数过多，验证码已失效")
            redis_client.hset(f'email_code:{email}', mapping={'counter': counter})
            data = {"retry_remaining": cfg["LOGIN_CODE_MAX_TRY"] - int(login_code_info["counter"]) -1}
            return CustomResponse(code=CustomStatus.LOGIN_CODE_MISS.value, msg="验证码错误", data=data)
        redis_client.delete(f'email_code:{email}')
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg=f"验证异常",data=str(e))
    # 保存用户数据
    try:
        user = User.query.filter_by(username=email).first()
        if user:
            # user.type = type
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return CustomResponse(msg="密码重置成功")
        realname = '用户' + str(uuid.uuid4())[:8]
        invitationCode = str(uuid.uuid4())[:8]
        avatar = f'https://q2.qlogo.cn/headimg_dl?dst_uin={email}&spec=640'
        user = User(username=email, realname=realname, enable=1,avatar=avatar,invitationCode=invitationCode)
        roles = Role.query.filter(Role.id.in_(['2'])).all()
        user.role = roles
        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        if invite_code:
            invite_user = User.query.filter_by(invitationCode=invite_code).first()
            if invite_user:
                inviteRecord = InviteRecord(inviter_id=invite_user.id,invitee_id=user.id)
                db.session.add(inviteRecord)
        db.session.commit()
        user.open_trial_membership()
        return CustomResponse(msg="注册成功")
    except SQLAlchemyError:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str('SQLAlchemyError'))
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str(e))

'''
登录接口
email:邮箱
password:密码
'''
@bp.post('/login')
@log_decorator
def login():
    # 验证数据
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        if email is None:
            return CustomResponse(code=CustomStatus.PARAM_ERROR.value,msg="请填写邮箱地址")
        if not verify_email(email):
            return CustomResponse(code=CustomStatus.EMAIL_FORMAT_MISALIGNMENT.value, msg="邮箱格式错误")
        if len(password) < 8:
            return CustomResponse(code=CustomStatus.PASSWORD_INSUFFICIENT_LENGTH.value, msg="密码长度必须至少为8个字符")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整",data=str(e))
    # 返回数据
    try:
        user = User.query.filter_by(username=email).first()
        if not user:
            return CustomResponse(code=CustomStatus.USER_NOT_FOUND.value,msg='用户不存在')

        if not user.validate_password(password):
            return CustomResponse(code=CustomStatus.AUTHENTICATION_FAILED.value, msg='密码错误')
        if user.enable == 0:
            return CustomResponse(code=CustomStatus.USER_BAN.value, msg='用户被封禁')

        # 更新用户身份
        if user.is_membership_expired():
            default_role = ['2']
            roles = Role.query.filter(Role.id.in_(default_role)).all()
            user.role = roles
            user.words = 0
            db.session.commit()
        # 获取token
        tokenData = {"userId": user.id}
        token = create_jwt_token(tokenData)
        role_names = [role.name for role in user.role][0]

        data = {
            'id': user.id,
            'username': user.username,
            "realname": user.realname,
            "token":token,
            'role_names':role_names,
            'avatar':user.avatar,
            'words':user.words,
            'diamonds':user.diamonds,
            'commission':user.commission,
            'membershipExpirationDate': user.membershipExpirationDate.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),

        }

        return CustomResponse(msg='登录成功',data=data)
    except SQLAlchemyError:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str('SQLAlchemyError'))
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg=f"服务端错误",data=str(e))

'''
快速获取验证码接口
email:邮箱
'''
@bp.post('/get_code')
@log_decorator
def get_code():
    email = request.json.get('email')
    redis_client = conn_redis_pool()
    login_code_info = redis_client.hgetall(f'email_code:{email}')
    return CustomResponse(msg="获取验证码成功",data=login_code_info)

'''
鉴权案例
'''
@bp.post('/other')
@token_required_decorator
@log_decorator
def other(userId):
    user = User.query.filter_by(id=str(userId)).first()

    roles = user.role.all()
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.password_hash,
        # 其他需要返回的用户信息
        "roles":roles[0].name
    }
    return CustomResponse(code=CustomStatus.PASSWORD_INSUFFICIENT_LENGTH.value, msg="success",data=data)


@bp.get('/get_state')
@token_required_decorator
@log_decorator
def get_state(userId):
    user = User.query.filter_by(id=str(userId)).first()
    if user.is_membership_expired():
        default_role = ['2']
        roles = Role.query.filter(Role.id.in_(default_role)).all()
        user.role = roles
        user.words = 0
        db.session.commit()
    data = {
        'id': user.id,
        'roles': [role.name for role in user.role][0],
        'words': user.words,
        'diamonds': user.diamonds,
        'create_at': user.create_at.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
        'membershipExpirationDate': user.membershipExpirationDate.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
    }
    return CustomResponse(code=CustomStatus.SUCCESS.value, msg='查询成功',data = data)

@bp.get('/is_vip')
@token_required_decorator
@log_decorator
def is_vip(userId):
    user = User.query.filter_by(id=str(userId)).first()
    if user.is_membership_expired():
        default_role = ['2']
        roles = Role.query.filter(Role.id.in_(default_role)).all()
        user.role = roles
        user.words = 0
        db.session.commit()
        return CustomResponse(code=CustomStatus.MEMBERSHIP_EXPIRED.value, msg='会员已过期')
    return CustomResponse(code=CustomStatus.SUCCESS.value, msg='会员')


@bp.post('/update_withdraw_info')
@token_required_decorator
@log_decorator
def withdraw_info(userId):
    try:
        alipay_account = request.json.get('alipay_account')
        alipay_name = request.json.get('alipay_name')
        if not alipay_account or not alipay_name:
            return CustomResponse(code=CustomStatus.INVALID_PARAMETER.value, msg='参数错误')
        user = User.query.filter_by(id=str(userId)).first()
        user.alipay_account = alipay_account
        user.alipay_name = alipay_name
        db.session.commit()
        return CustomResponse(msg='更新成功')
    except SQLAlchemyError:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误",data=str('SQLAlchemyError'))





