# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@File Name: test_call_create_client.py
@author: gaojie
@time:  2021/8/2 19:56
@function：
-------------------------------------------------
呼入、呼出、留言记录、满意度记录列表查询
"""

import os
import unittest

from common.handle_data import EnvData
from common.handle_excel import HandleExcel
from common.handle_request import HandleRequest
from library.myddt import ddt, data
from common.handle_path import DAILY_DIR_DATA

sheet_name = "test_call_jilu"
filename = os.path.join(DAILY_DIR_DATA, "call_apicases_daily.xlsx")


@ddt
class TestCallQueueTestCase(unittest.TestCase):
    excel = HandleExcel(filename, sheet_name)
    cases = excel.read_data()

    @data(*cases)
    def test_call_queue_common(self, case):
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        self.response = HandleRequest.request_response(case)
        if case['case_id'] == 1:
            IbUniqueId = self.response.json().get('cdrIbs')[0].get('uniqueId')
            setattr(EnvData, 'IbUniqueId', IbUniqueId)
        elif case['case_id'] == 4:
            ObUniqueId = self.response.json().get('cdrObs')[0].get('uniqueId')
            setattr(EnvData, 'ObUniqueId', ObUniqueId)
        status_code = self.response.status_code

        # 断言
        HandleRequest.assert_res(self, expected, status_code, case, self.response, self.excel, row)


if __name__ == '__main__':
    unittest.main()