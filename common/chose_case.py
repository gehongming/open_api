# -*- coding: utf-8 -*-
"""
@Time ： 2021/10/29 14:11
@Auth ： ghm
@File ：chose_case.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
from common.handle_path import *


class ChoseCase:

    def chosedir(self, case):
        """
        根据关键词执行对应的测试用例。
        """
        CaseInfoDict = {'daily': [DAILY_DIR, 'test*.py'],
                        'daily_crm': [DAILY_DIR, 'test_crm*.py'],
                        'daily_call': [DAILY_DIR, 'test_call*.py'],
                        'daily_cc': [DAILY_DIR, 'test_cc*.py'],
                        'daily_kbs': [DAILY_DIR, 'test_kbs*.py'],
                        'daily_c2': [DAILY_C2_DIR, 'test*.py'],
                        'daily_call_c2': [DAILY_C2_DIR, 'test_call*.py'],
                        'daily_crm_c2': [DAILY_C2_DIR, 'test_crm*.py'],
                        'daily_cc_c2': [DAILY_C2_DIR, 'test_cc*.py'], }
        try:
            DIR = CaseInfoDict[str(case)]
            return DIR
        except:
            return '该指令暂无效'


if __name__ == '__main__':
    print(ChoseCase().chosedir('adf'))