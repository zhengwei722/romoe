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
from applications.models import Role, Dept
from applications.models import User, AdminLog
from applications.common.utils.http import CustomResponse ,CustomStatus
import random
from flask_mail import Message
from applications.extensions import db, flask_mail
from applications.config import cfg
from sqlalchemy.exc import SQLAlchemyError
from aiosmtplib.errors import SMTPDataError
from applications.common.utils.redis import conn_redis_pool

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.post('/get_email_code')
def get_email_code():
    try:
        email = request.json.get('email')
        if email is None:
            return CustomResponse(code=CustomStatus.PARAM_ERROR.value, msg="请填写邮箱地址")
        # 验证email是否合法的email格式，是否有填写

        validate_email(email)
    except EmailNotValidError as e:
        return CustomResponse(code=CustomStatus.EMAIL_FORMAT_MISALIGNMENT.value, msg="邮箱格式错误")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整")
    try:
        user = User.query.filter_by(username=email).first()
        if user:
            return CustomResponse(code=CustomStatus.USERNAME_ALREADY_EXISTS.value, msg="用户已存在")

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
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误")
    except SMTPDataError:
        return CustomResponse(code=CustomStatus.OPERATE_DUPLICATE.value, msg="短时间内发送邮件次数过多，请稍后再试")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg=str(e))


#   用户分页查询
@bp.post('/register')
def register():
    try:
        email = request.json.get('email')
        email_code = request.json.get('email_code')
        password = request.json.get('password')
        confirm_password = request.json.get('confirm_password')
        if email is None:
            return CustomResponse(code=CustomStatus.PARAM_ERROR.value,msg="请填写邮箱地址")
        if password != confirm_password:
            return CustomResponse(code=CustomStatus.TWO_PASSWORDS_INCORRECT.value,msg="两次密码不一致")
        if email_code is None:
            return CustomResponse(code=CustomStatus.LOGIN_CODE_MISS.value,msg="请填写验证码")
        try:
            validate_email(email)
        except EmailNotValidError as e:
            return CustomResponse(code=CustomStatus.EMAIL_FORMAT_MISALIGNMENT.value, msg="邮箱格式错误")
        if len(password) < 8:
            return CustomResponse(code=CustomStatus.PASSWORD_INSUFFICIENT_LENGTH.value, msg="密码长度必须至少为8个字符")
    except Exception as e:
        return CustomResponse(code=CustomStatus.INCOMPLETE_DATA.value, msg="数据不完整")





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
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg=f"登录码验证异常:{str(e)}")



    try:
        user = User.query.filter_by(username=email).first()
        if user:
            return CustomResponse(code=CustomStatus.USERNAME_ALREADY_EXISTS.value, msg="用户已存在")
        user = User(username=email, realname=email, enable=1)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return CustomResponse(code=201, msg="注册成功")
    except SQLAlchemyError:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误")
    except Exception as e:
        return CustomResponse(code=CustomStatus.SERVER_ERROR.value, msg="服务端错误")




#   用户分页查询
@bp.post('/get_code')
def get_code():
    email = request.json.get('email')

    redis_client = conn_redis_pool()
    login_code_info = redis_client.hgetall(f'email_code:{email}')

    return {"data":login_code_info}