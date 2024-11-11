

from applications.config import cfg
import uuid
import hashlib
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import Flask, request, jsonify
from applications.models import User, AdminLog
from applications.common.utils.http import CustomResponse ,CustomStatus
from applications.common.utils.redis import conn_redis_pool
from applications.common.admin_log import api_log



SECRET_KEY = cfg["JWT_SECRET_KEY"]
ALGORITHM = cfg["JWT_ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(days=int(cfg["ACCESS_TOKEN_EXPIRE_MINUTES"]))

def create_jwt_token(data):
    """
    创建密钥
    :param data: 加密数据
    :return:
    """
    # 将用户id 用最安全的哈希 哈希后作为key, 加盐 盐在cfg里配置
    session_key = hashlib.sha256((str(data.get("userId")) + cfg["SESSION_SALT"]).encode()).hexdigest()
    # 生成客户端标识
    client_key = str(uuid.uuid4())
    data.update({"client_key": client_key})
    # 将用户id存入redis
    redis_client = conn_redis_pool()
    redis_client.setex(f"auth_token:{session_key}", ACCESS_TOKEN_EXPIRE_MINUTES, client_key)
    # 进行jwt加密
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token




def token_required_decorator(f):
    """
    一个装饰器，用于检查请求是否包含有效的 JWT 令牌。
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # 从请求头中获取令牌
        token = request.headers.get('Authorization')

        if not token:
            api_log(request, datetime.now(), datetime.now(), '0.00', {}, None, '令牌无效', is_access=True)
            return CustomResponse(code=CustomStatus.TOKEN_INVALID.value, msg=f"令牌无效")
        # 尝试解析令牌
        try:
            # 验证令牌并获取用户身份
            data = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            userId = data.get("userId")
            # 判断redis内是否存在该token
            redis_client = conn_redis_pool()
            session_key = hashlib.sha256((str(userId) + cfg["SESSION_SALT"]).encode()).hexdigest()
            client_key = redis_client.get(f"auth_token:{session_key}")
            if not client_key or client_key != data.get("client_key"):
                api_log(request, datetime.now(), datetime.now(), '0.00', {}, None, '令牌无效',is_access=True)
                return CustomResponse(code=CustomStatus.TOKEN_INVALID.value, msg=f"令牌无效")
            redis_client.expire(f"auth_token:{session_key}", ACCESS_TOKEN_EXPIRE_MINUTES)
        except:
            # 如果令牌无效或过期，返回错误响应
            api_log(request, datetime.now(), datetime.now(), '0.00', {}, None, '令牌无效', is_access=True)
            return CustomResponse(code=CustomStatus.TOKEN_INVALID.value, msg=f"令牌无效")

        # 将用户身份信息传递给原始函数
        kwargs['userId'] = userId
        return f(*args, **kwargs)

    return decorated
