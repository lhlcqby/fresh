#  生产订单方法.保证唯一性
import random
import time
def get_order_sn():
    s = '232fafdakirefjJSFKJIEJFALJDAJIJVFKNXNCIKLLJDFA34SLAO90'
    order_sn = ''
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())           # 加入时间戳
    return order_sn