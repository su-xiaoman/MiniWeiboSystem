 #!/usr/bin/env python
# -*- coding: utf-8 -*-


from email.mime.text import MIMEText
import smtplib
from email.utils import formataddr


def email(email_list,content,subject="新浪微博用户注册"):

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(content, 'plain', 'utf-8')

    msg['From'] = formataddr(["新浪科技","example@example.com"])
    msg['to'] = formataddr(["You",email_list])
    msg['Subject'] = subject

    try:
        print("正在尝试发送邮件")
        server = smtplib.SMTP()
        server.connect("example@example.com", 25)

        server.login("example@example.com","yourpassword") #两个参数，账号和密码
        server.sendmail('example@example.com',email_list,msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error：无法发送邮件")

if __name__ == '__main__':
    email('1369413407@qq.com',"感谢注册新浪微博，亲爱的用户，您的验证码为："+"123456")
