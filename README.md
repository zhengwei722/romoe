# readme

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
