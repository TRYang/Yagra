#!/usr/bin/python
import cgi
import cgitb
import os
import sys
import Cookie
import sha
import re

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def testMail(mail):
    return 0 if not re.match(
    r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", mail) else 1

def main():
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie.load(os.environ.get('HTTP_COOKIE'))
    if cookie.get('userid') == "":
        my_cgifunc.output_error(
            message="user error, please login in",
            back_page="index.py"
            )
        return
    if 'mail' in form and \
        'password' in form and \
        testMail(form['mail'].value):
        try:
            # get password from database and check the identity
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            cursor = mysql_connect.cursor()
            cursor.execute("""select * from UserInfo
                            where UserID = %d;""" %
                            int(cookie['userid'].value))
            result = cursor.fetchone()
            if result:
                password = sha.new(form['password'].value+result[5]).hexdigest()
                if password != result[2]:
                    raise Exception("Password is not right")
                cursor.execute("""select * from UserInfo
                                where EMail = '%s';""" %
                                form['mail'].value)
                if cursor.fetchone():
                    raise Exception("This E-mail address has been used, \
                            please use another one")
                cursor.execute("""update UserInfo set EMail = '%s'
                            where UserID = %d;""" %
                            (form['mail'].value, int(result[0])))
                cursor.execute("""update Cache set EMail = '%s'
                            where UserID = %d;""" %
                            (form['mail'].value, int(result[0])))
                mysql_connect.commit()
                cursor.close()
            else:
                raise Exception("connect to database error")
        except Exception, e:
            my_cgifunc.output_error(
                message=repr(e),
                back_page="/reset_mail.html"
                )
            return
        finally:
            mysql_connect.close()
        print cookie
        print my_cgifunc.content_type()
        print my_cgifunc.html_header('Reset email')
        print "<h1>Reset User:%s 's e-mail successful</h1>" % cookie['user'].value
        print "<form method=get action=showPage.py>"
        print '<input type=submit value="Back">'
        print "</form>"
        print my_cgifunc.html_tail()
    else:
        my_cgifunc.output_error(
            message="form data is not right!",
            back_page="/reset_mail.html"
            )

if __name__ == '__main__':
    main()
