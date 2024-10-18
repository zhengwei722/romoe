from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role
from applications.models import User, AdminLog,Appmodel

bp = Blueprint('appmodel', __name__, url_prefix='/appmodel')


# 用户管理
@bp.get('/')
@authorize("system:appmodel:main")
def main():
    return render_template('system/appmodel/main.html')


#   用户分页查询
@bp.get('/data')
@authorize("system:appmodel:main")
def data():

    # print(*filters)
    query = db.session.query(
        Appmodel
    ).layui_paginate()

    return table_api(
        data=[{
            'id': appmodel.id,
            'model_name': appmodel.model_name,
            'model_id': appmodel.model_id,
            'enable': appmodel.enable,
            'access_level': appmodel.access_level,
            'create_at': appmodel.create_at,
            'update_at':appmodel.update_at


        } for appmodel in query.items],
        count=query.total)

    # 用户增加


@bp.get('/add')
@authorize("system:appmodel:add", log=True)
def add():
    roles = Role.query.all()
    return render_template('system/appmodel/add.html', roles=roles)


@bp.post('/save')
@authorize("system:appmodel:add", log=True)
def save():
    req_json = request.get_json(force=True)
    a = req_json.get("roleIds")
    username = str_escape(req_json.get('username'))
    real_name = str_escape(req_json.get('realName'))
    password = str_escape(req_json.get('password'))
    role_ids = a.split(',')

    if not username or not real_name or not password:
        return fail_api(msg="账号姓名密码不得为空")

    if bool(User.query.filter_by(username=username).count()):
        return fail_api(msg="用户已经存在")
    user = User(username=username, realname=real_name,enable=1)
    user.set_password(password)
    db.session.add(user)
    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    for r in roles:
        user.role.append(r)
    db.session.commit()
    return success_api(msg="增加成功")


# 删除用户
@bp.delete('/remove/<int:id>')
@authorize("system:appmodel:remove", log=True)
def delete(id):
    user = User.query.filter_by(id=id).first()
    user.role = []

    res = User.query.filter_by(id=id).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


#  编辑用户
@bp.get('/edit/<int:id>')
@authorize("system:appmodel:edit", log=True)
def edit(id):
    user = curd.get_one_by_id(User, id)
    roles = Role.query.all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return render_template('system/appmodel/edit.html', user=user, roles=roles, checked_roles=checked_roles)


#  编辑用户
@bp.put('/update')
@authorize("system:appmodel:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    a = str_escape(req_json.get("roleIds"))
    id = str_escape(req_json.get("userId"))
    username = str_escape(req_json.get('username'))
    real_name = str_escape(req_json.get('realName'))

    password = str_escape(req_json.get('password'))
    balance = str_escape(req_json.get('balance'))
    if not a:
        return fail_api(msg="数据不完整")

    role_ids = a.split(',')
    User.query.filter_by(id=id).update({'username': username, 'realname': real_name,'balance':balance})
    u = User.query.filter_by(id=id).first()
    if password:
        u.set_password(password)
        db.session.add(u)

    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    u.role = roles

    db.session.commit()
    return success_api(msg="更新成功")





# 启用用户
@bp.put('/enable')
@authorize("system:appmodel:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = enable_status(model=User, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用用户
@bp.put('/disable')
@authorize("system:appmodel:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = disable_status(model=User, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")
