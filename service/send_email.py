# -*- coding: utf-8 -*-
import json

from env import CONF_PATH
import smtplib, os, pickle  # smtplib: 메일 전송을 위한 패키지
from email import encoders  # 파일전송을 할 때 이미지나 문서 동영상 등의 파일을 문자열로 변환할 때 사용할 패키지
from email.mime.text import MIMEText   # 본문내용을 전송할 때 사용되는 모듈
from email.mime.multipart import MIMEMultipart   # 메시지를 보낼 때 메시지에 대한 모듈
from email.mime.base import MIMEBase     # 파일을 전송할 때 사용되는 모듈

class Send_EMail:

    @classmethod
    def __init__(cls):
        with open(f'{CONF_PATH}/sender.info.json', 'r') as f:
            cls.info = json.load(f)
        print(cls.info)



    @classmethod
    def connect_to_mail_server(cls):
        cls.smtp = smtplib.SMTP_SSL(cls.info['smtp_server'], cls.info['smtp_port'])  # 서버의 포트번호
        cls.smtp.ehlo()
        cls.smtp.login(cls.info['smtp_id'], cls.info['smtp_pw'])

    @classmethod
    def send_email(cls, to, title, body):
        cls.connect_to_mail_server()
        msg = MIMEMultipart()  # msg obj.
        msg['Subject'] = title
        part = MIMEText(body, 'html')
        msg.attach(part)  # msg에 part obj.를 추가해줌
        msg['From']=cls.info['sender_email']
        msg['To']=to
        print(msg.as_string())
        cls.smtp.sendmail(cls.info['sender_email'], to, msg.as_string())
        cls.smtp.quit()


# Send_EMail().send_email('ssamkj@gmail.com', '오늘 ', 'olleh~~~')