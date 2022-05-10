# -*- coding: utf-8 -*-
"""
@Time ： 2021/11/12 17:09
@Auth ： ghm
@File ：base_utils.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""


import os
import unittest
import time
from jsonpath import jsonpath

from common.handle_excel import HandleExcel
from common.handle_request import HandleRequest
from library.myddt import ddt, data
from common.handle_path import *
from common.handle_data import EnvData
from common.config import *
config = ReadConfig()