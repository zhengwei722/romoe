from flask import Blueprint, request, render_template
from sqlalchemy import desc
from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.models import AdminLog
from applications.schemas import LogOutSchema,LogApiSchema
from applications.common.curd import model_to_dicts
from applications.common.utils.validate import str_escape
from applications.extensions import db
bp = Blueprint('log', __name__, url_prefix='/log')


# 日志管理
@bp.get('/')
@authorize("system:log:main")
def index():
    return render_template('system/admin_log/main.html')


# API日志
@bp.get('/apiLog')
@authorize("system:log:main")
def Api_log():
    date = str_escape(request.args.get('date', type=str))
    status = str_escape(request.args.get('status', type=str))

    filters = []
    if date:
        filters.append(AdminLog.starttime.like(f"{date}%"))
    if status:
        filters.append(AdminLog.success == int(status))


    log = db.session.query(
        AdminLog
    ).filter(*filters).order_by(desc(AdminLog.starttime)).layui_paginate()

    count = log.total

    return table_api(data= model_to_dicts(schema=LogApiSchema, data=log.items), count=count)



# 操作日志
# @bp.get('/systemLog')
# @authorize("system:log:main")
# def operate_log():
#     date = str_escape(request.args.get('date', type=str))
#     filters = []
#     if date:
#         filters.append(AdminLog.method.contains(date))
#     filters.append(AdminLog.url != '/system/passport/login')
#     log = db.session.query(
#         AdminLog
#     ).filter(*filters).layui_paginate()
#
#     count = log.total
#     return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)

