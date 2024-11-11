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
from datetime import datetime


def log_decorator(f):
    """
    一个装饰器，用于检查请求是否包含有效的 JWT 令牌。
    """
    @wraps(f)
    def decorated(*args, **kwargs):

        start_time = datetime.now()
        response = f(*args, **kwargs)

        end_time = datetime.now()
        total_time = "{:.2f}".format((end_time - start_time).total_seconds())

        user_id = kwargs.get('userId', None)

        response_dict = response.get_json()
        code = response_dict.get('code')
        tips = response_dict.get('msg')
        common_params = {
            'request': request,
            'start_time': start_time,
            'end_time': end_time,
            'total_time': total_time,
            'response_dict': response_dict,
            'user_id': user_id,
            'tips': tips
        }
        api_log(**common_params, is_access=code != 1000)

        return response

    return decorated