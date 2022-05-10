import unittest
from unittestreport import TestRunner

from common.config import *
from common.chose_case import ChoseCase
from common.do_consul import DoConsul
from common.handle_log import log
from common.handle_path import REPORT_DIR
import sys
config = ReadConfig()

# python -m run_test "test0" "daily_crm"

log.info('----------------用例执行开始--------------------')
env = sys.argv[-2]
WriteConfig().write(value=env)

dirs = sys.argv[-1]
DIR = ChoseCase().chosedir(dirs)

# 创建测试套件
suite = unittest.TestSuite()

# 加载用例到套件
loader = unittest.TestLoader()
# suite.addTest(loader.discover(CASE_DIR))
suite.addTest(loader.discover(DIR[0], pattern=DIR[1]))

runner = TestRunner(suite,
                    filename=f"clink2_{dirs}.html",
                    report_dir=REPORT_DIR,
                    title=f'clink2_{dirs}测试报告',
                    tester='demo',
                    desc=f"clink2_{dirs}接口测试报告",
                    templates=1)
# runner.run()

# 多线程
runner.run(thread_count=2)

# 发送钉钉通知
# runner.dingtalk_notice(url=config.get('dingding', 'url'),
#                        key=config.get('dingding', 'key'),
#                        secret=config.get('dingding', 'secret'))
# url=DoConsul().get_data()['url'],
# key=DoConsul().get_data()['key'],
# secret=DoConsul().get_data()['secret'])

runner.send_email(
    host=config.get('email', 'host'),
    port=465,
    user=config.get('email', 'user'),
    # password=DoConsul().get_data()["em_passwd"],
    password=config.get('email', 'password'),
    to_addrs=eval(config.get('email', 'to')))
log.info('----------------用例执行结束--------------------')

