import configparser
import os

from icecream import ic

from common import handle_path


class ReadConfig:

    def __init__(self):
        self.config=configparser.ConfigParser()
        self.config.read(handle_path.GLOBAL_FILE)
        switch = self.config.get('switch', 'on')  # 读取value
        file = os.path.join(handle_path.BASE_DIR, "conf", f'config_{switch.lower()}.ini')
        self.config.read(file, encoding='utf-8')

    def get(self, section, option):
        try:
            self.config.get(section,option)
        except:
            ic(f'配置文件下{section}没有{option}')
        return self.config.get(section,option)


config = ReadConfig()
if __name__ == '__main__':
    host = config.get("data", "tel")
    print(host)
    # number = int(config.get("data", "chatLimitNumber"))
    # print(number)