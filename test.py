# from applications.config import cfg
#
# print(cfg['MAIL_PASSWORD'],type(cfg['MAIL_PASSWORD']))
#
# from flask import Flask
# import redis
# from redis.exceptions import RedisError
#
# app = Flask(__name__)
#
# # 假设你的配置信息存储在 cfg 字典中
# cfg = {
#     'REDIS_HOST': 'your_redis_host',
#     'REDIS_PORT': 6379,  # Redis 端口号
#     'REDIS_PASSWORD': 'your_redis_password',  # Redis 密码，如果没有则为 None
#     'REDIS_DB': 0,  # 或者你想要连接的数据库编号
# }
#
#
# def conn_redis_pool():
#     """连接redis连接池"""
#     redis_pool = redis.ConnectionPool(
#         host=cfg['REDIS_HOST'],
#         port=cfg['REDIS_PORT'],
#         password=cfg['REDIS_PASSWORD'],
#         db=cfg['REDIS_DB'],
#         decode_responses=True  # 使用字符串响应，而不是字节
#     )
#     return redis.Redis(connection_pool=redis_pool)
#
#
# @app.route('/get_captcha')
# def get_captcha():
#     # 创建 Redis 连接
#     redis_client = conn_redis_pool()
#
#     # 假设验证码存储的键是 'captcha:<user_id>'
#     user_id = 'some_unique_user_id'
#     captcha_key = f'captcha:{user_id}'
#
#     # 生成一个随机验证码
#     captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#
#     # 将验证码保存到 Redis，并设置过期时间（例如300秒）
#     redis_client.setex(name=captcha_key, value=captcha_code, time=300)
#
#     # 返回验证码（在实际应用中，你可能需要返回验证码的图像或以其他方式发送给用户）
#     return captcha_code
#
#
# @app.route('/verify_captcha')
# def verify_captcha():
#     # 创建 Redis 连接
#     redis_client = conn_redis_pool()
#
#     # 获取用户输入的验证码
#     user_input_captcha = request.args.get('captcha', '')  # 假设验证码通过查询参数传递
#     user_id = 'some_unique_user_id'
#     captcha_key = f'captcha:{user_id}'
#
#     # 从 Redis 获取存储的验证码
#     stored_captcha = redis_client.get(captcha_key)
#
#     # 验证用户输入的验证码是否正确
#     if stored_captcha and stored_captcha.decode() == user_input_captcha:
#         # 验证成功，删除 Redis 中的验证码
#         redis_client.delete(captcha_key)
#         return '验证码正确'
#     else:
#         return '验证码错误或已过期'
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
import time
# 2024-10-12 02:38:05.352 | INFO     | __main__:tts:558 - 【['74850017-5d0c-4167-9548-f0990afb9f64', '6c29da60-0317-4a8f-8815-e4a118768738']】任务——任务类型：推理——任务状态：成功——开始时间：2024-10-12-02-38-01——结束时间：2024-10-12 02:38:05——共耗时：4.21秒——原因：None

from datetime import datetime

start_time = datetime.now()
print(start_time)
time.sleep(1)

end_time = datetime.now()
total_time = "{:.2f}".format((end_time - start_time).total_seconds())
print(total_time)