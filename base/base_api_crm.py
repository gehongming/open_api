from icecream import ic
from requests import request
from common.config import *
from common.handle_data import EnvData, MakeData
from common.handle_openapi import HandleOpenapi
from jsonpath import jsonpath
from common.handle_request import HandleRequest

expires = config.get("env", "expires")
headers = eval(config.get("env", "headers"))
ic.disable()


def list_customer_field():
    """获取必填的自定义客户字段"""
    api = HandleOpenapi(path="list_customer_field", method="GET")
    url = api.sign()
    get_response = request(method="GET", url=url, headers=headers)
    ic(get_response.text)
    a = get_response.json().get('customerFields')
    ic(a)
    list = []
    if len(a):
        for i in a:
            if i.get('required') == 1:
                if i.get('type') in (6, 9, 10,):
                    dict_1 = {'id': i.get('id'), 'value': i.get('property')[0].get('name')}
                    list.append(dict_1)
                elif i.get('type') in (7, 8):
                    dict_2 = {'id': i.get('id'), 'value': i.get('property')[0].get('title')}
                    list.append(dict_2)
                elif i.get('type') in (1, 2, 5):
                    dict_3 = {'id': i.get('id'), 'value': 17656565656}
                    list.append(dict_3)
                elif i.get('type') == 3:
                    dict_4 = {'id': i.get('id'), 'value': '101056@qq.com'}
                    list.append(dict_4)
                elif i.get('type') == 101:
                    dict_5 = {'id': i.get('id'), 'value': '323232323232323232'}
                    list.append(dict_5)
                elif i.get('type') == 102:
                    dict_6 = {'id': i.get('id'), 'value': '3232323232323232'}
                    list.append(dict_6)
                elif i.get('type') == 11:
                    dict_7 = {'id': i.get('id'), 'value': "2021/11/23 15:34:59"}
                    list.append(dict_7)
                elif i.get('type') == 12:
                    dict_8 = {'id': i.get('id'), 'value': "2021/11/23"}
                    list.append(dict_8)
                elif i.get('type') == 13:
                    dict_9 = {'id': i.get('id'), 'value': "15:35:01"}
                    list.append(dict_9)
                elif i.get('type') == 4:
                    dict_10 = {'id': i.get('id'), 'value': "121.1.1.1"}
                    list.append(dict_10)
        setattr(EnvData, "customize", list)
        return list
    else:
        setattr(EnvData, "customize", list)
        return []


class CrmBaseApi:

    @staticmethod
    def create_customer(re_cls):
        """创建客户资料"""
        # 请求地址
        api = HandleOpenapi(path="create_customer", method="POST")
        url = api.sign()
        data = {
            "name": '自动化测试请勿操作-公共',
            "tel": [MakeData.random_phone()],
            "level": 0,
            "shareType": 0,
            "share": None,
            "sex": 0,
            "email": "zhangsan@xxx.com.cn",
            "remark": '测试备注',
            "address": "河北省沧州市",
            "customize": list_customer_field(),
            "externalId": MakeData.random_externalId()
        }
        # 第二步：发送请求获取实际结果
        response = request(method="POST", url=url, json=data, headers=headers)
        res = response.json()
        print(res)
        try:
            customer_id = jsonpath(res, "$..id")[0]
        except:
            print(f'请求失败：{res}')
        setattr(re_cls, 'customer_id', customer_id)
        return customer_id

    @staticmethod
    def delete_customer(customer_id):
        """删除客户资料"""
        # 请求地址
        api = HandleOpenapi(path="delete_customer", method="POST")
        url = api.sign()
        data = {
            "id": customer_id
        }
        # 第二步：发送请求获取实际结果
        response = request(method="POST", url=url, json=data, headers=headers)
        res = response.json()
        customer_id = jsonpath(res, "$..id")[0]
        return customer_id


if __name__ == '__main__':
    print(list_customer_field())
