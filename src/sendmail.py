#!/usr/bin/python
# coding: UTF-8
import os
import cgi
import cgitb
import smtplib
import re
from email.mime.text import MIMEText

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def testMail(mail):
    return 0 if not re.match(
    r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mail) else 1

def send_mail(tolist, subject, content):
    me = ''.join((my_conf.Server_mail,
                '<',
                my_conf.Server_mail,
                '@',
                my_conf.Server_mail_postfix,
                '>'))
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = ';'.join(tolist)
    try:
        client = smtplib.SMTP()
        client.connect(my_conf.Server_mail_host)
        client.login(my_conf.Server_mail, my_conf.Server_mail_password)
        client.sendmail(me, tolist, msg.as_string())
        client.close()
        return True
    except Exception, e:
        return False

def main():
    form = cgi.FieldStorage()
    if 'Mail' in form and testMail(form['Mail'].value):
        # get the user information according to the mail address
        user = ""
        userid = 0
        finger = ""
        try:
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            cursor = mysql_connect.cursor()
            cursor.execute("""select * from UserInfo
                            where EMail = '%s';""" %
                            form['Mail'].value)
            result = cursor.fetchone()
            cursor.close()
            if not result:
                raise Exception('E-mail address error!')
            user = result[1]
            userid = int(result[0])
            finger = result[2]
        except Exception, e:
            my_cgifunc.output_error(
                    message=repr(e),
                    back_page='/findout.html'
                    )
            return
        finally:
            mysql_connect.close()

        tolist = (form['Mail'].value)
        subject = """Please reset your password in Yagra"""
        content = """
    Hi %s:
        please click below link to reset your password in Yagra:
            http://%s:%s/cgi-bin/findout.py?userid=%d&finger=%s

    Please delete this e-mail after reset your password as soon as possible.
    If you have any question about Yagra, please send mail to '%s' to contact administrator %s.
                  """ % (
                user,
                os.environ.get('SERVER_NAME'),
                os.environ.get('SERVER_PORT'),
                userid,
                finger,
                my_conf.AdminEMail,
                my_conf.AdminName
                )
        if send_mail(tolist, subject, content):
            print my_cgifunc.content_type()
            print my_cgifunc.html_header('Success')
            print """已发送找回密码的邮件到您的邮箱，请尽快查收"""
            print """<form method=get action=/index.html>
                        <input type=submit value="首页">
                    </form>"""
            print my_cgifunc.html_tail()
        else:
            my_cgifunc.output_error(
                    message="Send mail failed!",
                    back_page="/findout.html"
                    )
    else:
        my_cgifunc.output_error(
                message="Mail information is not right!",
                back_page="/findout.html"
                )

if __name__ == '__main__':
    main()
