#!/bin/python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os 

class Message(object):

    def format_str(self,strs):
        if not isinstance(strs, unicode) :
            strs = unicode(strs)
        return strs

    def __init__(self, from_user, to_user, subject, content, with_attach=False):
        
        if with_attach:
            self._message = MIMEMultipart() 
            self._message.attach(MIMEText(content, 'plain','utf-8'))
        else:
            self._message = MIMEText(content, 'plain','utf-8')
        
        self._message['Subject'] = Header(subject,'utf-8')
        self._message['From'] = Header(self.format_str(from_user),'utf-8')
        self._message['To'] = Header(self.format_str(to_user), 'utf-8')
        self._with_attach = with_attach


    def attach(self, file_path):
        if self._with_attach == False:
            print "Please init the Message with attr 'with_attach = True'"
            exit(1)
        if os.path.isfile(file_path) == False:
            print "The file doesn`t exist!"
            exit(1)
        atta = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        atta['Content-Type'] = 'application/octet-stream'
        atta['Content-Disposition'] = 'attachment; filename="%s"' % Header(os.path.basename(file_path),'utf-8')
        self._message.attach(atta)

    def getMessage(self):
        return self._message.as_string()

class SMTPClient(object):

    def __init__(self,hostname,port,user,passwd):
        self._HOST = hostname
        self._USER = user
        self._PASS = passwd
        self._PORT = port

    def send(self, sender, receivers, msg):
        if isinstance(msg, Message) == False:
            print "Error Message Instance!"
            exit(1)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self._HOST, self._PORT)
            smtpObj.login(self._USER,self._PASS)  
            smtpObj.sendmail(sender, receivers, msg.getMessage())
            return (1, "邮件发送成功")
        except smtplib.SMTPException,e:
            return (0, "Error: 无法发送邮件%s"%e)

if __name__ == '__main__':
    # smpt_client = SMTPClient('smtp.cstnet.cn',25,'kongdefei@ict.ac.cn','kong19920213')
    # msg = Message("KDF5000",'kongdefei','你好吗','中午有空吗？')
    # smpt_client.send('kongdefei@ict.ac.cn',['kongdefei@ict.ac.cn'],msg)

    smpt_client = SMTPClient('smtp.cstnet.cn',25,'kongdefei@ict.ac.cn','kong19920213')
    msg = Message("kongdefei@ict.ac.cn",'kdf5000@kindle.cn','菊与刀.mobi','菊与刀.mobi',with_attach=True)
    msg.attach("./菊与刀.mobi")
    print msg.getMessage()
    print smpt_client.send('kongdefei@ict.ac.cn',['kdf5000@kindle.cn'],msg)
