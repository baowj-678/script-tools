# -*- coding: UTF-8 -*-
import time
import requests
import smtplib
from email.mime.text import MIMEText
import argparse
import yaml
import logging
import re

### mail setting
mail_host = "smtp.163.com"
mail_user = "test@163.com"
mail_pass = "test"
mail_subject = "test"
mail_content = "test！！！"
mail_receiver = "test@qq.com"

mail_message = MIMEText(mail_content, "plain", "utf-8")
mail_message['Subject'] = mail_subject
mail_message['To'] = mail_receiver
mail_message['From'] = mail_user

### page setting
url = "https://www.baidu.com"
s = "baidu"


def check(path, regex):
    text = requests.get(path).text
    if len(regex.findall(text)) > 0:
        return True
    return False


def monitor(url, s, t):
    regex = re.compile(s)
    while True:
        if check(url, regex):
            logging.info("check true")
            mail_to()
            return
        logging.info("still listening")
        time.sleep(t)


def mail_login():
    smtp = smtplib.SMTP_SSL("smtp.163.com", 994)
    smtp.login(mail_user, mail_pass)
    logging.info("login mail client")
    return smtp


def mail_to():
    ### mail login
    smtp = mail_login()
    ### send mail
    logging.info("send mail from (" + mail_user + ") to (" + mail_receiver + ") with (" + mail_message.as_string() + ")")
    smtp.sendmail(mail_user, [mail_receiver], mail_message.as_string())
    ### mail close
    mail_close(smtp)


def mail_close(smtp):
    logging.info("close mail client")
    smtp.close()


def mail_config(path):
    data = None
    with open(path, 'r', encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    ### mail message reset
    global mail_host
    global mail_user
    global mail_pass
    global mail_subject
    global mail_content
    global mail_receiver
    global mail_message

    mail_host = data['mail_host']
    mail_user = data['mail_user']
    mail_pass = data['mail_pass']
    mail_subject = data['mail_subject']
    mail_content = data['mail_content']
    mail_receiver = data['mail_receiver']

    mail_message = MIMEText(mail_content, "plain", "utf-8")
    mail_message['Subject'] = mail_subject
    mail_message['To'] = mail_receiver
    mail_message['From'] = mail_user


if __name__ == '__main__':
    ### logging init
    logging.basicConfig(format='[%(levelname)s] %(asctime)s: %(message)s', level=logging.INFO)

    ### parse args
    parser = argparse.ArgumentParser()
    parser.description = 'please enter two parameters url, str and config ...'
    parser.add_argument("-u", "--url", help="the url to page", dest="url", type=str, default=url)
    parser.add_argument("-s", "--str", help="the string to match", dest="sstr", type=str, default=s)
    parser.add_argument("-c", "--config", help="the config path", dest="config", type=str, default="config.yaml")
    parser.add_argument("-t", "--time", help="listening gap time", dest="time", type=int, default=60)
    args = parser.parse_args()

    ### load config
    mail_config(args.config)

    ### monitoring
    monitor(args.url, args.sstr, args.time)

