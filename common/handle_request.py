import json
import time
import jmespath
import urllib3
from icecream import ic
from requests import request
from unittest import TestCase

from common.handle_openapi import HandleOpenapi
from common.handle_log import log
from common.handle_context import Context
from common.handle_data import EnvData
from common.config import *


class HandleRequest:
    @staticmethod
    def request_response(case, re_cls):
        """
        判断接口请求，并返回响应的返回值
        :return: response结果
        """
        headers = eval(config.get("env", "headers"))
        sms_headers = eval(config.get("env", "sms_headers"))

        # 请求方法
        method = case["method"]
        path = case["interface"]
        time.sleep(int(case.get('sleep'))) if case.get('sleep') else time.sleep(0)
        if not case.get("skip"):
            data = Context().re_replace_new(case['data'],re_cls=re_cls)
            if method == "GET":
                api = HandleOpenapi(path=path, method=method)
                if data == 'None':
                    url = api.sign()
                else:
                    url = api.sign(s=data)
                log.info(f"用例--{case['title']}请求url：{url}")
                log.info(f"用例--{case['title']}请求数据：{data}")
                response = request(method=method, url=url, headers=headers, timeout=8)
            elif method == "POST":

                api = HandleOpenapi(path=path, method=method)
                url = api.sign()
                log.info(f"用例--{case['title']}请求url：{url}")
                log.info(f"用例--{case['title']}请求数据：{data}")
                data = eval(data)
                if case["content-type"] == "json":
                    response = request(method=method, url=url, json=data, headers=headers, timeout=20)
                elif case["content-type"] == "form-data":
                    response = request(method=method, url=url, files=data, timeout=20)
                else:
                    response = request(method=method, url=url, json=data, headers=sms_headers, timeout=20)
            else:
                return "Method is not 'GET' or 'POST'"
            par = case.get('jsonpath_exp_save')
            # from common.handle_data import EnvData
            if par:
                re_par = EnvData().re_par_new(eval(par), response.json(), re_cls=re_cls)
                print(re_par)
            return response
        else:
            log.info("用例跳过")
            response = request(method='post', url='http://www.baidu.com')
            return response

    @staticmethod
    def clink2_request(case, re_cls):
        """常规页面接口专用"""
        # 测试数据进行转换,替换参数
        time.sleep(int(case.get('sleep'))) if case.get('sleep') else time.sleep(0)
        if not case.get("skip"):
            if case.get('data'):
                data = json.loads(Context().re_replace_new(case["data"]))
                log.info(f"用例--{case['title']}请求数据：{data}")
            # 获取用例中的请求方法、平台
            method = case["method"]
            target = case['target'].lower()
            # 根据客户端不同 获取不同的cookies, url
            cookies = Context().re_replace_new({"Cookie": f"#{target}_cookie#"})
            cookies = json.loads(cookies.replace("'", '"'))

            url = Context().re_replace_new(case["interface"])
            url = config.get('env', f"base_{target}_url") + url

            log.info(f"用例--{case['title']}---请求url：{url}")
            # 请求方法。
            if method.lower() in ['get', 'delete']:
                resp = request(method=method, url=url, cookies=cookies, verify=False)
            elif method.lower() in ['post', 'put']:
                if case["content-type"] == "json":
                    resp = request(method=method, url=url, json=data, cookies=cookies, verify=False)
                else:
                    resp = request(method=method, url=url, data=data, cookies=cookies, verify=False)
            par = case.get('jsonpath_exp_save')
            if par:
                from common.handle_data import EnvData
                if par != None:
                    re_par = EnvData().re_par_new(eval(par), resp.json())
                    print(re_par)
            return resp
        else:
            log.info("用例跳过")
            response = request(method='post', url='http://www.baidu.com')
            return response

    @staticmethod
    def assert_res(self, expected, status_code, case, response, excel, row, actual=None):
        """
        断言方法的封装
        """
        if not case.get('skip'):
            if expected.get("json"):
                jsons = expected.get("json")
                actual = HandleRequest.actual_json(actual, response.json())
            else:
                jsons = None
                actual = None
            try:
                TestCase.assertEqual(self, expected["status_code"], status_code)
                TestCase.assertEqual(self, jsons, actual)
                log.info(f"用例--{case['title']}--执行通过")
            except AssertionError as e:
                log.error(f"用例--{case['title']}--执行未通过")
                log.exception(e)
                # 结果回写excel中
                # excel.write_data(row=row, column=8, value="未通过")
                raise e
            log.info(f"用例--{case['title']}预期结果：{expected}")
            log.info(f"用例--{case['title']}实际结果：{response.text}")
        #     else:
        #         # 结果回写excel中
        #         # excel.write_data(row=row, column=8, value="通过")
        else:
            log.info(f"用例--{case['title']}--用例跳过")

    @staticmethod
    def actual_json(actual, jsons):
        """
        actual：列表格式，存放比对的字段key名
        jsons：实际的返回值
        """
        p = []
        for l in actual:
            q = jmespath.search(l, jsons)
            p.append(q)
        return p