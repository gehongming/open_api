import configparser
import re
from common.config import *
from common.handle_log import log
config = ReadConfig()


class Context:

    p = '#(.*?)#'  # 正则表达式

    def re_replace_new(self, data, re_cls=None):
        data = str(data)  # 把数据强制转换成str，其他格式会报错
        while re.search(self.p, data):
            # print(data)
            # 从任意位置开始找，找第一个就返回Match object, 如果没有找None
            m = re.search(self.p, data)
            g = m.group(1)
            # print(g)
            try:
                v = config.get('data', g)  # 根据KEY取配置文件里面的值
            except configparser.NoOptionError as e:
                log.info(f"配置文件下--data--没有--{g}")
                from common.handle_data import EnvData
                if hasattr(re_cls, g):
                    v = str(getattr(re_cls, g))  # 如果被替换的值是int，会报错，需要转换果格式
                elif hasattr(EnvData, g):
                    v = str(getattr(EnvData, g))
                else:
                    raise e
            data = re.sub(self.p, v, data, count=1)  # 替换
        return data


def replace(para, old, new):
    if para.find(old) != -1:  # para中找到old
        # print(para.find(old))
        data = para.replace(old, new)
        return data
    else:
        return para


if __name__ == '__main__':
    # from common.handle_excel import HandleExcel
    # import os
    # from common.handle_path import DATA_DIR
    # from common.handle_request import HandleRequest
    # sheet_name = "test_call_queue"
    # filename = os.path.join(DATA_DIR, 'daily', "call_apicases_daily.xlsx")
    # excel = HandleExcel(filename, sheet_name)
    # cases = excel.read_data()[0]
    # print(cases)
    # print(a.re_replace(cases))
    a = Context()
    print(a.re_replace_new('#endTime#'))