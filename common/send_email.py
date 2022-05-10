# -*- coding: utf-8 -*-
"""
-------------------------------------------------
@File Name: send_email.py
@author: gaojie
@time:  2021/8/2 19:56
@function：
-------------------------------------------------
"""

import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from common.handle_path import REPORT_DIR
from common.config import *
config = ReadConfig()


def send_email():
    # 第一步：连接到smtp服务器
    smtp = smtplib.SMTP_SSL(config.get("email", "host"), port=465)
    smtp.login(user=config.get("email", "user"), password=config.get("email", "password"))
    # 第二步：构造一封多组间邮件
    msg = MIMEMultipart()
    msg["Subject"] = "在线客服OpenApi测试报告"
    msg["To"] = "gaojie_122@163.com"
    msg["From"] = config.get("email", "from")
    # 构建邮件的文本内容
    text = MIMEText("您好，如下为在线客服OpenApi测试报告，请查收", _charset="utf-8")
    msg.attach(text)
    # 构建邮件内容
    with open(os.path.join(REPORT_DIR, "OpenApi.html"), "rb") as f:
        content = f.read()
    report = MIMEApplication(content, _charset="utf-8")
    report.add_header('content-disposition', 'attachment', filename='OpenApi.html')
    msg.attach(report)

    # 第三步：发送邮件
    smtp.send_message(msg, from_addr=config.get("email", "from"), to_addrs=eval(config.get("email", "to")))
