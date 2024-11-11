from flask_login import current_user

from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import AdminLog


def login_log(request, uid, is_access):
    info = {
        'method': request.method,
        'url': request.path,
        'ip': request.remote_addr,
        'user_agent': str_escape(request.headers.get('User-Agent')),
        'desc': str_escape(request.form.get('username')),
        'uid': uid,
        'success': int(is_access)

    }
    log = AdminLog(
        url=info.get('url'),
        ip=info.get('ip'),
        user_agent=info.get('user_agent'),
        desc=info.get('desc'),
        uid=info.get('uid'),
        method=info.get('method'),
        success=info.get('success')
    )
    db.session.add(log)
    db.session.flush()
    db.session.commit()
    return log.id


def api_log(request, start_time,end_time,total_time,response_dict, user_id,tips,is_access):
    try:
        request_data = request.json if request.headers.get('Content-Type') == 'application/json' else request.values
    except:
        request_data = {}

    info = {
        'method': request.method,
        'uid':user_id,
        'url': request.path,
        'request_body': str(dict(request_data)),
        'response':str(response_dict),
        'start_time': start_time,
        'end_time': end_time,
        'total_time': total_time,
        'success': int(is_access),
        'tips':tips

    }
    log = AdminLog(
        method=info.get('method'),
        uid=info.get('uid'),
        url=info.get('url'),
        request_body=info.get('request_body'),
        response_body=info.get('response'),
        starttime=info.get('start_time'),
        endtime=info.get('end_time'),
        totaltime=info.get('total_time'),
        success=info.get('success'),
        tips=info.get('tips')
    )
    try:
        db.session.add(log)
        db.session.flush()
        db.session.commit()

        return log.id
    except:
        db.session.rollback()
        return None
