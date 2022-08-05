# -*- coding: utf-8 -*-
"""
@Time ： 2022/8/4 16:09
@Auth ： ghm
@File ：myresult.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)

"""
import logging
from io import StringIO
import sys
import traceback
import time
from unittestreport.core.testResult import TestResult


class MyResult(TestResult):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('tr')

    def startTest(self, test):
        super().startTest(test)
        # ----add logging output-----fancc
        self.log_cap = StringIO()
        self.ch = logging.StreamHandler(self.log_cap)
        self.ch.setLevel(logging.DEBUG)
        myfmt = logging.Formatter(
            '%(asctime)s - %(name)s - "%(filename)s: %(lineno)d" - %(funcName)s - %(levelname)s - %(message)s')
        self.ch.setFormatter(myfmt)
        self.logger.addHandler(self.ch)

    def complete_output(self):
        if self.sys_stdout:
            sys.stdout = self.sys_stdout
            sys.stderr = self.sys_stdout
            self.sys_stdout = None
            self.sys_stdout = None
        # add log out put ---------fancc
        return self.outputBuffer.getvalue() + '\n' + self.log_cap.getvalue()

    def stopTest(self, test):
        super().stopTest(test)
        # 清除log的handle----fancc
        self.logger.removeHandler(self.ch)


class MyReRunResult(MyResult):
    def __init__(self, count, interval):
        super().__init__()
        self.count = count
        self.interval = interval
        self.run_cases = []

    def startTest(self, test):
        if not hasattr(test, "count"):
            super().startTest(test)

    def stopTest(self, test):
        if test not in self.run_cases:
            self.run_cases.append(test)
            super().stopTest(test)

    def addFailure(self, test, err):
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            sys.stderr.write("{}执行——>【失败Failure】\n".format(test))
            for string in traceback.format_exception(*err):
                sys.stderr.write(string)
            sys.stderr.write("================{}重运行第{}次================\n".format(test, test.count))

            time.sleep(self.interval)
            test.run(self)
        else:
            super().addFailure(test, err)
            if test.count != 0:
                sys.stderr.write("================重运行{}次完毕================\n".format(test.count))

    def addError(self, test, err):
        if not hasattr(test, 'count'):
            test.count = 0
        if test.count < self.count:
            test.count += 1
            sys.stderr.write("{}执行——>【错误Error】\n".format(test))
            for string in traceback.format_exception(*err):
                sys.stderr.write(string)
            sys.stderr.write("================{}重运行第{}次================\n".format(test, test.count))
            time.sleep(self.interval)
            test.run(self)
        else:
            super().addError(test, err)
            if test.count != 0:
                sys.stderr.write("================重运行{}次完毕================\n".format(test.count))




