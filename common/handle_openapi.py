# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@File Name: handle_openapi.py
@author: gaojie
@time:  2021/8/2 19:56
@function：
-------------------------------------------------
"""

import os
import time
from datetime import datetime
from urllib.parse import quote
from urllib import parse
import hmac
from hashlib import sha1
import base64

from common.do_consul import DoConsul
from urllib.parse import urlencode
from common.config import *
config = ReadConfig()


protocol = config.get("env", "protocol")
host = config.get("env", "host")
expires = config.get("env", "expires")
# access_key_secret = DoConsul().get_data()["accessKeySecret"]
# access_key_id = DoConsul().get_data()["accessKeyId"]
access_key_secret = config.get("env", "accessKeySecret")
access_key_id = config.get("env", "accessKeyId")


class HandleOpenapi:
    """生成请求openapi的请求地址"""

    def __init__(self, path, method, protocol=protocol, host=host, expires=expires, access_key_secret=access_key_secret,
                 access_key_id=access_key_id):
        # 获取时间戳并进行url转码
        timestamp = quote(HandleOpenapi.get_utc_time())
        self.path = path
        self.method = method
        self.timestamp = timestamp

    def sign(self, s=None):
        # 排序后url
        if s:
            s = HandleOpenapi.encoded_params(param=s)
            temp_url = host + "/" + self.path + "?AccessKeyId=" + access_key_id + "&Expires=" + expires + \
                       "&Timestamp=" + self.timestamp + "&" + s
        else:
            temp_url = host + "/" + self.path + "?AccessKeyId=" + access_key_id + "&Expires=" + expires + \
                       "&Timestamp=" + self.timestamp
        # print("排序编码后url:",temp_url)
        url_param = self.method + temp_url
        # 对签名进行url编码
        signature = quote(HandleOpenapi.hash_hmac(url_param, access_key_secret, sha1))
        # 加上签名后的url
        result = temp_url + '&Signature=' + signature
        res = protocol + "://" + result
        # print("加上签名后的url:", res)
        return res

    @staticmethod
    def get_utc_time():
        """
        #     获取当前时间，返回iso 8601格式的时间戳
        #     :return: 返回iso 8601格式的时间戳
        #     """
        time1 = datetime.utcfromtimestamp(int(time.time()))
        utc_time = time1.strftime("%Y-%m-%dT%H:%M:%SZ")
        return utc_time

    @staticmethod
    def hash_hmac(code, key, sha1):
        """
        HMACSHA1加密，返回Base64编码
        :param code:
        :param key:
        :param sha1:
        :return:
        """
        hmac_code = hmac.new(key.encode(), code.encode(), sha1).digest()
        return base64.b64encode(hmac_code).decode()

    @staticmethod
    def encoded_params(param):
        dic = parse.parse_qs(param)

        for key in dic:
            s = dic[key][0]
            dic[key] = s

        encoded_data = urlencode(dic)
        return encoded_data


if __name__ == '__main__':
    # api = HandleOpenapi(path='copy_chat_records', method='GET')
    api = HandleOpenapi(path='list_ticket_workflow', method='GET',)
    ur = api.sign(s='category=3325&limit=10&offset=')
    # s = "offset=0&limit=10"

    print(ur)


