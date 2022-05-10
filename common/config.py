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
            return self.config.get(section,option)


class WriteConfig:

    def __init__(self):
        self.config=configparser.ConfigParser()
        self.config.read(handle_path.GLOBAL_FILE,encoding='utf-8')

    def write(self, value, section='switch', option='on'):
            self.config.read(handle_path.GLOBAL_FILE)
            self.config.set(section, option, value)
            file_global = os.path.join(handle_path.GLOBAL_FILE)
            with open(file_global, 'w') as wf:
                self.config.write(wf)


if __name__ == '__main__':
    config = ReadConfig()
    host = config.get("data", "tel")
    print(host)
    # number = int(config.get("data", "chatLimitNumber"))
    # print(number)