
from alipay.utils import AliPayConfig
from alipay import AliPay
import datetime
import random
from applications.config import cfg
app_private_key_string = open("./applications/common/utils/private_key.txt").read()
alipay_public_key_string = open("./applications/common/utils/public_key.txt").read()

# 应用私钥格式
"""
-----BEGIN RSA PRIVATE KEY-----
base64 encoded content
-----END RSA PRIVATE KEY-----
"""
# 支付宝公钥格式
"""
-----BEGIN PUBLIC KEY-----
base64 encoded content
-----END PUBLIC KEY-----
"""

alipay = AliPay(
    appid=cfg['APPID'],
    app_notify_url=None,  # 默认回调 url
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",  # RSA 或者 RSA2
    debug=True,  # 默认 False
    verbose=True,  # 输出调试数据
    config=AliPayConfig(timeout=15)  # 可选，请求超时时间
)

def get_pay_url(trade_no,amount,trade_name):
    res = alipay.api_alipay_trade_page_pay(
        out_trade_no=trade_no,  # 订单号
        total_amount=amount,  # 价格
        subject=trade_name,  # 名称
        return_url=cfg['RETURN_URL'],  # 支付成功后会跳转的页面
        notify_url=cfg['NOTIFY_URL'],  # 回调地址，支付成功后支付宝会向这个地址发送post请求
    )
    #正式环境 gataway = 'https://openapi.alipay.com/gateway.do?'
    # 沙盒环境
    gataway = cfg['GATWAY_URL']
    pay_url = gataway + res # 支付链接
    return pay_url

def verify_pay(data,sign):
    success = alipay.verify(data,sign)  # True False
    if success and data['trade_status'] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        return True
    return False




def changeUserIdentity():
    pass

def changeUserBalance():
    pass

def generate_order_id():
    # 获取当前日期和时间
    now = datetime.datetime.now()
    # 格式化日期为年月日小时分钟秒
    date_str = now.strftime("%Y%m%d%H%M%S")
    # 生成一个随机数
    random_num = random.randint(1000, 9999)
    # 将日期和随机数拼接成订单号
    order_id = f"{date_str}{random_num}"
    return order_id