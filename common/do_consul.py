#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@File Name:learning_yaml
@author:yangjuan
@time: 2020/7/22
@function：
-------------------------------------------------
"""

import yaml
import consul
from common.config import *
config = ReadConfig()


class DoConsul:

    def __init__(self, scheme='http'):  # DoYaml初始化函数，连接concul

        self.host = config.get('consul', 'host')
        self.port = config.get('consul', 'port')
        self.consulPath = config.get('consul', 'consulPath')
        self.token = config.get('consul', 'token')

        try:
            self.c = consul.Consul(host=self.host, port=self.port, token=self.token,scheme=scheme)

        except Exception as e:
            # 读取配置文件失败
            print('Failed to establish a new connection')
            raise e

    def get_data(self):
        config = self.c.kv.get(self.consulPath, index=0, token=self.token)
        data = config[1]['Value'].decode()
        data = yaml.load(data, Loader=yaml.FullLoader)
        return data


if __name__ == '__main__':

    data = DoConsul().get_data()["em_passwd"]
    print(data)



