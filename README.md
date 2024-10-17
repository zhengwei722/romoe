# readme

<div align="center">
<br/>
<br/>
  <h1 align="center">
    Pear Admin Flask
  </h1>
  <h4 align="center">
    开 箱 即 用 的 Flask 快 速 开 发 平 台
  </h4>

  [预览](http://flask.pearadmin.com:8000)   |   [官网](http://www.pearadmin.com/)   |   [群聊](docs/assets/qqgroup.jpg)   |   [文档](docs/detail.md)

<p align="center">
    <a href="#">
        <img src="https://img.shields.io/badge/pear%20admin%20flask-1.0.0-green" alt="Pear Admin Layui Version">
    </a>
    <a href="#">
        <img src="https://img.shields.io/badge/Python-3.6+-green.svg" alt="Python Version">
    </a>
      <a href="#">
        <img src="https://img.shields.io/badge/Mysql-5.3.2+-green.svg" alt="Mysql Version">
    </a>
</p>
</div>

<div align="center">
  <img  width="92%" style="border-radius:10px;margin-top:20px;margin-bottom:20px;box-shadow: 2px 0 6px gray;" src="https://images.gitee.com/uploads/images/2020/1019/104805_042b888c_4835367.png" />
</div>

# 项目简介

Pear Admin Flask 基于 Flask 的后台管理系统，拥抱应用广泛的python语言，通过使用本系统，即可快速构建你的功能业务
项目旨在为 python 开发者提供一个后台管理系统的模板，可以快速构建信息管理系统。

项目使用 flask-sqlalchemy + 权限验证 + marshmallow 序列化与数据验证，以此方式集成了若干不同的功能。

# 内置功能

- [x] 用户管理：用户是系统操作者，该功能主要完成系统用户配置。
- [x] 权限管理：配置系统菜单，操作权限，按钮权限标识等。
- [x] 角色管理：角色菜单权限分配。
- [x] 操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
- [x] 登录日志：系统登录日志记录查询包含登录异常。
- [x] 服务监控：监视当前系统CPU、内存、磁盘、python版本,运行时长等相关信息。
- [x] 文件上传:   图片上传示例

# 项目分支说明

> **⚠️注意** Pear Admin Flask 不仅仅只提供一种对于 Pear Admin 后端的实现方式，所以提供了不同的分支版本，不同分支版本各有其优劣，并且由不同的开发者维护。

| 分支名称                                                             | 特点                     |
|------------------------------------------------------------------|------------------------|
| master（您目前浏览的分支版本）                                               | 功能齐全，处于开发阶段，代码量较大。     |
| [main](https://gitee.com/pear-admin/pear-admin-flask/tree/main/) | 功能精简，代码量小，处于开发阶段，易于维护。 |
| [mini](https://gitee.com/pear-admin/pear-admin-flask/tree/mini/)    | 不再更新，是最初版本的镜像。         |


> **⚠️注意** 由于 master 分支项目需要，暂时移除了 Flask-APScheduler 定时任务 功能。

# 版本支持情况

经过测试，此项目的（master分支）运行要求是 `>= Python 3.8` ，推荐使用 `Python 3.9`。

> **💡提示** 由于 Flask 中使用的 Werkzeug 模块更新，Flask 官方并未进行更新，所以可能会出现 ImportError 。
> 此类情况的出现可以通过正确安装 `requirements.txt` 中的模块（以及其对应版本）解决。

# 项目结构

## 应用结构

```应用结构
Pear Admin Flask
├─applications  # 应用
│  ├─extensions  # 注册插件
│  ├─models  # 数据模型
│  ├─static  # 静态资源文件
│  ├─templates  # 静态模板文件
│  └─views  # 视图部分
│     ├─admin  # 后台管理视图模块
│     └─index  # 前台视图模块
├─docs  # 文档说明
├─migrations  # 迁移文件记录
├─requirement  # 依赖文件
└─.env # 项目的配置文件
```

## 资源结构

```资源结构
Pear Admin Flask
├─static    # 项目设定的 Flask 资源文件夹
│  ├─admin    # pear admin flask 的后端资源文件（与 pear admin layui 同步）
│  ├─index    # pear admin flask 的前端资源文件
│  └─upload     # 用户上传保存目录
└─templates # 项目设定的 Flask 模板文件夹
  ├─admin   # pear admin flask 的后端管理页面模板
  │  ├─admin_log    # 日志页面
  │  ├─common       # 基本模板页面（头部模板与页脚模板）
  │  ├─console      # 系统监控页面模板
  │  ├─dept         # 部门管理页面模板
  │  ├─dict         # 数据自动页面模板
  │  ├─mail         # 邮件管理页面模板
  │  ├─photo        # 图片上传页面模板
  │  ├─power        # 权限（菜单）管理页面模板
  │  ├─role         # 角色管理页面模板
  │  ├─task         # 任务设置页面模板
  │  └─user         # 用户管理页面模板
  ├─errors  # 错误页面模板
  └─index   # 主页模板
```

# 项目安装

## 从仓库获取

```bash
# 克隆仓库 / 手动下载
git clone https://gitee.com/pear-admin/pear-admin-flask
cd pear-admin-flask  # 进入到项目目录
```

## 修改配置

> **💡提示** 配置文件位于  `applications/config.py` ，打开配置文件看到的是位于 `BaseConfig` 类下的默认配置文件，您可以编写自己的配置类并继承 `BaseConfig` 类。
项目启动时，会调用 `applications/__init__.py` ，这个文件中加载了程序的配置，所以在您编写了自己的类后不要忘记在文件 `applications/__init__.py` 中修改使用的配置类。

> **⚠️注意** 配置文件中对于数据库的配置有所更改，请查看代码中的注释修改配置。

```python
# 部分配置信息如下所示

# 验证密钥（⚠️ 一定要记得修改 ⚠️）
SECRET_KEY = "pear-system-flask"

# 数据库的配置信息
SQLALCHEMY_DATABASE_URI = 'sqlite:///../pear.db'

# 默认日志等级
LOG_LEVEL = logging.WARN

# flask-mail配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = '123@qq.com'
MAIL_PASSWORD = 'XXXXX'  # 生成的授权码
MAIL_DEFAULT_SENDER = MAIL_USERNAME
```


## 虚拟环境安装项目（推荐）

> **💡提示** 为了保证项目所依赖的库不影响其他部署在同一主机上的项目，我们推荐使用虚拟环境安装。

```bash
python -m venv venv

# 进入虚拟环境下
venv\Scripts\activate.bat  # Windows 提示命令符
venv\Scripts\Activate.ps1  # Windows Powershell
. venv/bin/activate  # Linux

# 使用 pip 安装
pip install -r requirements.txt
```

## 直接安装项目

```bash
# 使用 pip 安装
pip install -r requirements.txt
# 同时你可以选择以模块的方式调用 pip
python -m pip install -r requirements.txt
```

# 运行项目

+ 一般情况运行项目

```bash
# 初始化数据库
flask db init
flask db migrate
flask db upgrade
flask admin init

# 运行项目
flask --app app.py run -h 0.0.0.0 -p 8000 --debug

# 或者直接调用 app.py
python app.py
```

+ 使用 docker-compose 运行项目

```bash
git clone https://gitee.com/pear-admin/pear-admin-flask

# 安装 docker-compose 
curl -L https://github.com/docker/compose/releases/download/1.26.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose 

# 运行如下命令，有输出版本，表示 docker-compose 可以用了
docker-compose --version 

# 在当前目录执行如下命令即可以运行 app
docker-compose -f dockercompose.yaml up

# 看到如下表示运行成功，由于 pip 下载慢，需要一些时间，请耐心等待；如果安装失败，重新执行上面的命令即可。

# 运行后在浏览器访问 127.0.0.1:5000 

#如果要停止容器运行，在当前文件夹执行如下命令：
docker-compose -f dockercompose.yaml down
```







## 本地环境准备
在开始本项目前，你需要在自己的电脑上准备就绪以下这些环境:  
1. mysql
2. redis
3. python 

备注:  
1. 本地 mysql 的 用户名/密码 需要配置好  
1. redis 需要开启 requirepass 并设置一个账户: `AUTH <username> <password>`  

## 本地配置准备
在上述工作准备好了后，即可开始配置本地的环境:  
1. 在工程目录中创建文件 `env_local.toml`  
1. 将 `env.yaml` 中的内容复制到 `env_local.yaml`  
1. 修改 `env_local.yaml` 中的 redis 与 数据库 配置为自己本地环境的配置  
1. 在 `env_local.yaml` 的中加上如下配置(该配置直接询问对接的人进行获取):  
```env_local.toml
# 测试服务器链接配置
DEV_SSH_HOST=xxx
DEV_SSH_PASSWORD=xxx

# 本地版本声明(会在本地执行 `CUSTOM_ENV_TOML=env_local.toml uvicorn main:app --host 0.0.0.0 --port 10001` 启动时自动增加 /api/v2 的路径映射)
VERSION=local
```

## 数据导入
在上述工作准备好了后，即可开始进行本地数据的初始化工作:
1. 确认工程的依赖安装就绪 `pip install -r requirements.txt`  
1. 执行 `python bin/backup_db_dev.py` 将测试环境的 db 备份到本地(路径为 <本工程路径>/prompt_tool.sql，备份会耗费一定的时间)  
1. 将上述 sql 导入到自己本地的 mysql 中即可（运作正常会发现本地的 mysql 多了一个名为 prompt_tool 的 db）  

## 服务启动
在上述工作准备好了后，即可执行 python app.py 启动服务



## 发布到测试环境
当完成相关功能的开发后，需要给前端使用时，可执行 `python bin/deploy_dev.py` 将工程发布到测试环境

备注：  
1. 该发布方式会覆盖当前测试环境运行的版本  
1. 所以发布后最好在交流群里告知以下，让其他协作者知道当前的部署

## 与前端的实时联调
实时联调简要说明:  
1. 采用的主要策略是使用 frp 做内网映射，完成开发者内网环境的可联调  
1. 每名参与后端的开发者都有不同的测试环境端口分配，以便于并行开发/调试  

相关软件准备:  
1. 这里使用的是 frp 0.51.3 版本  
1. 在官方的 release 界面下载需要的版本: https://github.com/fatedier/frp/releases/tag/v0.51.3  
1. 下载后将其中的 frpc 文件加入到执行路径，并在本地建立如下的链接配置文件(frpc.ini)  
```ini
# frpc.ini 链接配置文件
[common]
server_addr = 测试环境ip地址
server_port = 7000
token = frps链接token(向已参与后端开发的同事询问)

[proxy]
type = tcp
local_ip = 127.0.0.1
local_port = 10001
remote_port = 后端组协商分配给你的独有调试端口
```

配置完成后本地在上述 frpc.ini 文件所在的目录中执行 frpc -c frpc.ini 即可将本地启动的后端服务暴露到公网，供前端进行实时的测试联调  

补充说明  
1. 在 win 场景下 frpc 文件会被识别为病毒，需要手动屏蔽报警，具体原因参考: https://github.com/fatedier/frp/issues/2860  



备注:
1. 工程的 readme 文档主要作为参与后端开发成员的 startup，主要服务于让新加入的后端成员快速进入开发节奏的目标  
1. 其他和工程相关的说明文档则放在 /docs 目录下，如有新编辑的和 startup 有关的内容则放在 readme 中，其他说明则放在 /docs 中  
1. 文档中不要带有安全敏感内容(如ip, 密码等)  

## git提交注意事项
1.开发新功能时，首先pull master分支最新代码，然后新建个人分支，在个人分支上开发
2.开发完成后，自测通过后，提交代码到个人分支的远程分支，等待远端rebase到dev分支，然后合并到dev分支做回归测试
3.dev测试通过后，代表新功能开发完毕。
4.下次开发新功能时，不要基于前一次的个人分支，需要基于dev分支（pull）建立新的个人分支
