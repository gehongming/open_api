# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@File Name: handle_config.py
@author: gaojie
@time:  2021/8/2 19:56
@function：
-------------------------------------------------
"""

import os
from configparser import ConfigParser
from common.handle_path import CONF_DIR


class HandleConfig(ConfigParser):
    """配置文件解析器类的封装"""

    def __init__(self, filename):
        super().__init__()
        self.read(filename, encoding="utf8")


conf = HandleConfig(os.path.join(CONF_DIR, "config.ini"))
