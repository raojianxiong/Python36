#coding=utf-8
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib

def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,"utf-8").encode(),addr))

#发件人地址
from_addr = "**"
#密码
password = "**"
#收件人
to_addr = "***"
#163网易邮件服务器地址
smtp_server = "smtp.163.com"
#信息
msg = MIMEText('<html><body><h1>Hello</h1><p>异常网页<a href="http://www.baidu.com"/></p></body></html>','html','utf-8')
msg['from'] = _format_addr('Python爱好者 <%s>'%from_addr)
msg['to'] = _format_addr('Python爱好者 <%s>'%to_addr)
msg['Subject'] = Header('Python邮件回复','utf-8').encode()

#发送邮件
server = smtplib.SMTP(smtp_server,25)
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,[to_addr],msg.as_string())
server.quit()