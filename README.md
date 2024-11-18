# readme

<div align="center">
<br/>
<br/>
  <h1 align="center">
    ROMOE
  </h1>


  [预览](http://flask.pearadmin.com:8000)   |   [官网](http://www.guijiyunai.com/)   |   [群聊](docs/assets/qqgroup.jpg)   |   [文档](docs/detail.md)


</div>



# 项目简介

.......



# 项目分支说明

> **⚠️注意** prod生产环境代码，dev开发环境代码，master主分支，在主分支的代码中新建分支，进行开发

| 分支名称                                                             | 特点                     |
|------------------------------------------------------------------|------------------------|
| master   | 主分支     |
| prod | 生产环境 |
| dev   | 开发环境代码        |



# 版本支持情况

经过测试，此项目的（master分支）运行要求是 `>= Python 3.8` ，推荐使用 `Python 3.10`。

> **💡提示** 由于 Flask 中使用的 Werkzeug 模块更新，Flask 官方并未进行更新，所以可能会出现 ImportError 。
> 此类情况的出现可以通过正确安装 `requirements.txt` 中的模块（以及其对应版本）解决。

# 项目结构

## 应用结构

```应用结构
Pear Admin Flask
├─applications  # 应用
│  ├─common    # 文件
│  ├─extensions  # 注册插件
│  ├─models  # 数据模型
│  └─views  # 视图部分
│     ├─system  # 后台管理视图模块
│     └─api  # 接口视图模块
├─docs  # 文档说明
├─static  # 静态资源文件
├─templates  # 静态模板文件
├─migrations  # 迁移文件记录
├─requirement  # 依赖文件
└─.yaml # 项目的环境配置文件
```


# 项目安装

## 从仓库获取

```bash
# 克隆仓库 / 手动下载
git https://github.com/zhengwei722/romoe
cd romoe  # 进入到项目目录
```

## 修改配置


> **⚠️注意** 配置文件中对于数据库的配置有所更改，请查看代码中的注释修改配置。

```python
# 部分配置信息如下所示

# redis配置
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = '123456'
REDIS_DB = 15

# mysql 配置
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "123456"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "romoe"
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




# 数据导入【下面内容待更新】





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
