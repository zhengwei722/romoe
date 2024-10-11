from flask import Flask
import redis
from flask import request
from applications.config import cfg


def conn_redis_pool():
    """连接redis连接池"""
    redis_pool = redis.ConnectionPool(
        host=cfg['REDIS_HOST'],
        port=cfg['REDIS_PORT'],
        password=cfg['REDIS_PASSWORD'],
        db=cfg['REDIS_DB'],
        decode_responses=True  # 使用字符串响应，而不是字节
    )
    return redis.Redis(connection_pool=redis_pool)

