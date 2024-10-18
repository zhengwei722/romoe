from flask import jsonify


def success_api(msg: str = "成功"):
    """ 成功响应 默认值“成功” """
    return jsonify(success=True, msg=msg)


def fail_api(msg: str = "失败"):
    """ 失败响应 默认值“失败” """
    return jsonify(success=False, msg=msg)


def table_api(msg: str = "", count=0, data=None, limit=10):
    """ 动态表格渲染响应 """
    res = {
        'msg': msg,
        'code': 0,
        'data': data,
        'count': count,
        'limit': limit

    }
    return jsonify(res)

def CustomResponse(data=None, code=200, msg=""):
    # 如果没有提供data或者data为False，只返回msg和code
    if data is None or data == {} or data == []:
        res = {'msg': msg, 'code': code,'data': {}}
    else:
        res = {'msg': msg, 'code': code, 'data': data}
    return jsonify(res)

from enum import Enum

class CustomStatus(Enum):
    # 成功
    SUCCESS = 0
    # 服务端错误
    SERVER_ERROR = 1000
    #数据不完整Incomplete data
    INCOMPLETE_DATA = 1001
    # 令牌过期
    TOKEN_EXPIRED = 4001
    # 令牌无效
    TOKEN_INVALID = 4002
    # 参数无效
    INVALID_PARAMETER = 4003
    # 新增操作违规状态码
    OPERATE_ILLEGAL = 4004
    # 余额不足
    INSUFFICIENT_BALANCE = 4005
    # 文件不存在
    FILE_NOT_FOUND = 4006
    # 操作重复
    OPERATE_DUPLICATE = 4007
    # 权限不足
    INSUFFICIENT_AUTHORITY = 4008
    # 不能删除默认收藏夹
    CANNOT_DELETE_SYSTEM_FOLDER = 4009
    # 用户已经拥有最大数量的收藏夹
    TOO_MANY_FOLDERS = 4010
    # 收藏夹操作权限不足
    INSUFFICIENT_PERMISSIONS_FOR_THE_FOLDER = 4011
    # 已达到最大收藏数量
    MAXIMUM_NUMBER_OF_COLLECTIONS_REACHED = 4012
    # 文本审查失败
    TEXT_REVIEW_FAILED = 4013
    # 本月投稿数量已达到最大值
    MAXIMUM_NUMBER_OF_CONTRIBUTIONS_REACHED = 4014
    # 不能投稿别人的作品
    CANNOT_CONTRIBUTE_OTHER_WORKS = 4015


    # 验证码错误
    PARAM_ERROR = 5001
    #两次密码不一致
    TWO_PASSWORDS_INCORRECT = 5002
    # 未找到登陆码
    LOGIN_CODE_MISS = 5003
    # 尝试登陆次数过多
    LOGIN_CODE_TO_MANY_TRY = 5004
    # 没找到用户
    USER_NOT_FOUND = 5005
    # 用户封禁
    USER_BAN = 5006
    # 邮箱格式错误
    EMAIL_FORMAT_MISALIGNMENT = 5007
    # 用户名已经存在
    USERNAME_ALREADY_EXISTS = 5008
    # 密码长度不够Insufficient length
    PASSWORD_INSUFFICIENT_LENGTH = 5009
    # 身份验证失败
    AUTHENTICATION_FAILED = 5010