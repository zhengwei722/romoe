import datetime

from flask.cli import AppGroup

from applications.extensions import db
from applications.models import User, Role, Power

admin_cli = AppGroup("admin")

now_time = datetime.datetime.now()
userdata = [
    User(
        id=1,
        username='admin',
        password_hash='pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85',
        create_at=now_time,
        enable=1,
        realname='超级管理',
        avatar='/static/system/admin/images/avatar.jpg',
        balance=0.0
    ),
    User(
        id=2,
        username='test',
        password_hash='pbkdf2:sha256:150000$cRS8bYNh$adb57e64d929863cf159f924f74d0634f1fecc46dba749f1bfaca03da6d2e3ac',
        create_at=now_time,
        enable=1,
        realname='测试',
        avatar='/static/system/admin/images/avatar.jpg',
        balance=0.0

    ),
]
roledata = [
    Role(
        id=1,
        code='admin',
        name='管理员',
        enable=1,
        details='管理员',
        sort=1,
        create_time=now_time,
    ),
    Role(
        id=2,
        code='common',
        name='普通用户',
        enable=1,
        details='只有查看，没有增删改权限',
        sort=2,
        create_time=now_time,
    )
]

powerdata = [
    Power(
        id=1,
        name='系统管理',
        type='0',
        code='',
        url=None,
        open_type=None,
        parent_id='0',
        icon='layui-icon layui-icon-set-fill',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=3,
        name='用户管理',
        type='1',
        code='system:user:main',
        url='/system/user/',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon layui-icon layui-icon layui-icon-rate',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=31,
        name='模型管理',
        type='1',
        code='system:appmodel:main',
        url='/system/appmodel/',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon layui-icon layui-icon layui-icon-rate',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=32,
        name='订单管理',
        type='1',
        code='system:paylist:main',
        url='/system/paylist/',
        open_type='_iframe',
        parent_id='2',
        icon='layui-icon layui-icon layui-icon layui-icon layui-icon-rate',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=4,
        name='权限管理',
        type='1',
        code='system:power:main',
        url='/system/power/',
        open_type='_iframe',
        parent_id='1',
        icon=None,
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=9,
        name='角色管理',
        type='1',
        code='system:role:main',
        url='/system/role',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-username',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=12,
        name='系统监控',
        type='1',
        code='system:monitor:main',
        url='/system/monitor',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-vercode',
        sort=5,
        create_time=now_time,
        enable=1,

    ), Power(
        id=13,
        name='日志管理',
        type='1',
        code='system:log:main',
        url='/system/log',
        open_type='_iframe',
        parent_id='1',
        icon='layui-icon layui-icon-read',
        sort=4,
        create_time=now_time,
        enable=1,

    ),  Power(
        id=21,
        name='权限增加',
        type='2',
        code='system:power:add',
        url='',
        open_type='',
        parent_id='4',
        icon='layui-icon layui-icon-add-circle',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=22,
        name='用户增加',
        type='2',
        code='system:user:add',
        url='',
        open_type='',
        parent_id='3',
        icon='layui-icon layui-icon-add-circle',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=23,
        name='用户编辑',
        type='2',
        code='system:user:edit',
        url='',
        open_type='',
        parent_id='3',
        icon='layui-icon layui-icon-rate',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=24,
        name='用户删除',
        type='2',
        code='system:user:remove',
        url='',
        open_type='',
        parent_id='3',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=25,
        name='权限编辑',
        type='2',
        code='system:power:edit',
        url='',
        open_type='',
        parent_id='4',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=26,
        name='用户删除',
        type='2',
        code='system:power:remove',
        url='',
        open_type='',
        parent_id='4',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=27,
        name='用户增加',
        type='2',
        code='system:role:add',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=1,
        create_time=now_time,
        enable=1,

    ), Power(
        id=28,
        name='角色编辑',
        type='2',
        code='system:role:edit',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=2,
        create_time=now_time,
        enable=1,

    ), Power(
        id=29,
        name='角色删除',
        type='2',
        code='system:role:remove',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=3,
        create_time=now_time,
        enable=1,

    ), Power(
        id=30,
        name='角色授权',
        type='2',
        code='system:role:power',
        url='',
        open_type='',
        parent_id='9',
        icon='',
        sort=4,
        create_time=now_time,
        enable=1,

    )



]


def add_user_role():
    admin_role = Role.query.filter_by(id=1).first()
    admin_user = User.query.filter_by(id=1).first()
    admin_user.role.append(admin_role)
    test_role = Role.query.filter_by(id=2).first()
    test_user = User.query.filter_by(id=2).first()
    test_user.role.append(test_role)
    db.session.commit()


# def add_role_power():
#     admin_powers = Power.query.filter(Power.id.in_([1, 3, 4, 9, 12, 13, 17, 18, 44, 48])).all()
#     admin_user = Role.query.filter_by(id=2).first()
#     for i in admin_powers:
#         admin_user.power.append(i)
#     db.session.commit()


@admin_cli.command("init")
def init_db():
    db.session.add_all(userdata)
    print("加载系统必须用户数据")
    db.session.add_all(roledata)
    print("加载系统必须角色数据")
    db.session.add_all(powerdata)
    print("加载系统必须权限数据")
    db.session.commit()
    print("基础数据存入")
    add_user_role()
    print("用户角色数据存入")
    # add_role_power()
    print("角色权限数据存入")
    print("数据初始化完成,请使用run脚本运行")
