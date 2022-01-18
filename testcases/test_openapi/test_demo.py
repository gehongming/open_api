# -*- coding: utf-8 -*-
"""
知识库目录查询正向用例：需要手动增加知识库目录。
"""

from base_utils import *


sheet_name = "demo"
filename = os.path.join(DAILY_DIR_DATA, "test_demo.xlsx")


@ddt
class TestDemoTestCase(unittest.TestCase):
    excel = HandleExcel(filename, sheet_name)
    cases = excel.read_data()

    @data(*cases)
    def test_directories_common(self, case):
        expected = case["expected"]
        actual = case['actual']
        row = case["case_id"] + 1
        self.response = HandleRequest.request_response(case, TestDemoTestCase)

        status_code = self.response.status_code

        # 断言
        HandleRequest.assert_res(self, expected, status_code, case, self.response, self.excel, row, actual)


if __name__ == '__main__':
    unittest.main()
