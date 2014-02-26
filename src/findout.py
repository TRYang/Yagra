#!/usr/bin/python
# coding: UTF-8
import cgi
import cgitb

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def main():
    form = cgi.FieldStorage()
    if 'userid' in form and 'finger' in form:
        try:
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            # check the finger
            cursor = mysql_connect.cursor()
            cursor.execute("""select * from UserInfo
                        where UserID = %d;""" % int(form['userid'].value))
            result = cursor.fetchone()
            cursor.close()
            if not result or result[2] != form['finger'].value:
                raise Exception
        except Exception, e:
            my_cgifunc.output_error(
                    message="link error, please contact the admin again",
                    back_page="/index.html"
                    )
            return
        finally:
            mysql_connect.close()

        print my_cgifunc.content_type()
        print my_cgifunc.html_header('Reset password')
        print """
            <FORM METHOD=POST ACTION=reset_withoutpass.py>
                <INPUT TYPE=HIDDEN VALUE="%s" NAME="UserID">
                <INPUT TYPE=HIDDEN VALUE="%s" NAME="Finger">
                <B>输入新密码：</B>
                <INPUT TYPE=PASSWORD NAME="new_password">
                <br/>
                <B>再次输入新密码：</B>
                <INPUT TYPE=PASSWORD NAME="password_again">
                <br/>
                <INPUT TYPE=SUBMIT VALUE="提交">
                <INPUT TYPE=RESET VALUE="重置">
            </FORM>
              """ % (form['userid'].value, form['finger'].value)
        print my_cgifunc.html_tail()
    else:
        my_cgifunc.output_error(
                message="link error, please contact the admin again",
                back_page="/index.html"
                )

if __name__ == '__main__':
    main()
