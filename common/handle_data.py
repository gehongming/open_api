import datetime
import random, string, time
import jmespath


class MakeData:

    @staticmethod
    def get_current_stamp():
        """获取当天的开始时间，结束时间戳"""
        # 今天日期
        today = datetime.date.today()
        # 昨天时间
        yesterday = today - datetime.timedelta(days=1)
        # 明天时间
        tomorrow = today + datetime.timedelta(days=1)
        acquire = today + datetime.timedelta(days=2)
        # 昨天开始时间戳
        yesterday_start_time = int(time.mktime(time.strptime(str(yesterday), '%Y-%m-%d')))
        # 昨天结束时间戳
        yesterday_end_time = int(time.mktime(time.strptime(str(today), '%Y-%m-%d'))) - 1
        # 今天开始时间戳
        today_start_time = str(yesterday_end_time + 1)
        # 今天结束时间戳
        today_end_time = str(int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) - 1)
        # # 明天开始时间戳
        # tomorrow_start_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d')))
        # # 明天结束时间戳
        # tomorrow_end_time = int(time.mktime(time.strptime(str(acquire), '%Y-%m-%d'))) - 1
        # 当前时间时间戳（毫秒）
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        today_time = int(str(int(time.mktime(time.strptime(ts, '%Y-%m-%d %H:%M:%S')))) + '000')
        # 获取格式化日期2021-09-03
        date = time.strftime("%Y-%m-%d", time.localtime())
        # 获取形如2021-09-03 18:59:59的时间
        date_start_time = date + " 00:00:00"
        date_end_time = date + " 23:59:59"
        # YYMMDD格式的日期20210903
        date1 = date.split("-")
        today_date = ''.join(date1)

        return today_start_time, today_end_time, date, today_date, date_start_time, date_end_time, today_time

    @staticmethod
    def random_phone():
        """生成一个手机号"""
        while True:
            phone = "139"
            number = random.randint(10000000, 99999999)
            phone += str(number)
            return phone

    @staticmethod
    def random_externalId():
        num = str(random.randint(1000, 9999))
        src_uppercase = string.ascii_uppercase  # string_大写字母
        src_lowercase = string.ascii_lowercase  # string_小写字母
        chrs = random.sample(src_lowercase + src_uppercase, 3)
        for i in chrs:
            num += i
        return num



class EnvData:
    """
    用于参数传递，获取动态参数
    """
    a = MakeData()
    date_time = a.get_current_stamp()
    startTime = date_time[0]
    endTime = date_time[1]
    updateStartTime = date_time[0]
    updateEndTime = date_time[1]
    date = date_time[3]
    dateStartTime = date_time[4]
    dateEndTime = date_time[5]
    today_time = date_time[-1]
    name = "新增客户资料" + str(time.time())
    tels = a.random_phone()
    externalId = a.random_externalId()

    def re_par_new(self, par, resp, re_cls):
        """
        par: jsonpath_exp_save 列表嵌套字典
        resp：请求返回值
        re_cls：用例类
        作用：jsonpath_exp_save提取特定返回值，并存储于特定类的属性中
        """
        error_list = []
        if isinstance(par, list):
            for exp in par:
                for k, v in exp.items():
                    cashu = jmespath.search(v, resp)
                    if cashu:
                        setattr(re_cls, k, cashu)
                    elif cashu == 0:
                        setattr(re_cls, k, cashu)
                    else:
                        setattr(re_cls, k, None)
                        error_list.append(k)
            if error_list:
                return (f'转换成功,该字段--{error_list}--没有正常转换，手动转为None')
            else:
                return ('转换成功')
        else:
            return (f'{par}格式错误')


if __name__ == '__main__':
   setattr(EnvData, 'DEMO', None)
   print(type(getattr(EnvData, 'DEMO')))



