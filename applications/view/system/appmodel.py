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
import pytz
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
            'create_at': appmodel.create_at.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S'),
            'update_at':appmodel.update_at.astimezone(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')


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
    # roleIds = req_json.get("roleIds")
    modelName = str_escape(req_json.get('modelName'))
    modelId = str_escape(req_json.get('modelId'))
    access_level = str_escape(req_json.get('access_level'))
    if not access_level or not modelName or not modelId:
        return fail_api(msg="模型名称，ID，权限不得为空")
    if bool(Appmodel.query.filter_by(model_name=modelName).count()):
        return fail_api(msg="模型已经存在")
    appmodel = Appmodel(model_name=modelName, model_id=modelId,access_level=access_level,enable=1)
    db.session.add(appmodel)
    db.session.commit()
    return success_api(msg="增加成功")


# 删除用户
@bp.delete('/remove/<int:id>')
@authorize("system:appmodel:remove", log=True)
def delete(id):
    appmodel = Appmodel.query.filter_by(id=id).delete()
    db.session.commit()
    if not appmodel:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


#  编辑用户
@bp.get('/edit/<int:id>')
@authorize("system:appmodel:edit", log=True)
def edit(id):
    appmodel = curd.get_one_by_id(Appmodel, id)
    # roles = Role.query.all()
    # checked_roles = []
    #
    # checked_roles.append(appmodel.access_level_id)
    # print(checked_roles)
    return render_template('system/appmodel/edit.html', appmodel=appmodel)


#  编辑用户
@bp.put('/update')
@authorize("system:appmodel:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    access_level = str_escape(req_json.get("access_level"))
    appmodelId = str_escape(req_json.get("appmodelId"))
    model_name = str_escape(req_json.get('model_name'))
    model_id = str_escape(req_json.get('model_id'))

    if not access_level or not appmodelId or not model_name or not model_id:
        return fail_api(msg="模型名称，ID，权限不得为空")

    # if roleIds:
    #     return fail_api(msg="数据不完整")
    #
    #
    Appmodel.query.filter_by(id=appmodelId).update({'model_name': model_name, 'model_id': model_id,'access_level':access_level})
    # u = User.query.filter_by(id=id).first()
    #
    #
    # roles = Role.query.filter(Role.id.in_(role_ids)).all()
    # u.role = roles
    #
    db.session.commit()
    return success_api(msg="更新成功")





# 启用用户
@bp.put('/enable')
@authorize("system:appmodel:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = enable_status(model=Appmodel, id=_id)
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
        res = disable_status(model=Appmodel, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")
