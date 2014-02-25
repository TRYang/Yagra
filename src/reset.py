#!/usr/bin/python
import os
import sys
import cgi
import cgitb
import Cookie
import sha

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display = 0, logdir = my_conf.CGI_log_dir)

def main():
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie.load(os.environ.get('HTTP_COOKIE'))
    if cookie.get('userid') == "":
        my_cgifunc.output_error(message="user error, please login in again.",
                        back_page="index.py")
        return
    if 'old_password' in form and \
        'new_password' in form and \
        'password_again' in form and \
        form['new_password'].value == form['password_again'].value:
        try:
            # get password from database and check the identity
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            cursor = mysql_connect.cursor()
            cursor.execute("""select * from UserInfo where UserID = %d;""" %
                            int(cookie['userid'].value))
            result = cursor.fetchone()
            old_password = sha.new(form['old_password'].value).hexdigest()
            new_password = sha.new(form['new_password'].value).hexdigest()
            if result and result[2] == old_password:
                cursor.execute("""update UserInfo set Password = '%s'
                                  where UserID = %d;""" % (
                            new_password, int(cookie['userid'].value)))
                mysql_connect.commit()
                print my_cgifunc.content_type()
                print my_cgifunc.html_header("Reset success")
                print "<h1>Reset user(%s) password successful!</h1>" % \
                        cookie['user'].value
                print """<FORM METHOD=GET ACTION=showPage.py>
                        <INPUT TYPE=SUBMIT VALUE="Back">
                        </FORM>"""
                print my_cgifunc.html_tail()
            else:
                if not result:
                    raise Exception("fetch user information from database error!")
                elif result[2] != old_password:
                    raise Exception("old password is not right!")
                else:
                    raise Exception("something error")
        except Exception, e:
            my_cgifunc.output_error(message = repr(e),
                            back_page="/reset_password.html")
        finally:
            mysql_connect.close()
    else:
        my_cgifunc.output_error(message="password information error!",
                        back_page="/reset_password.html")

if __name__ == '__main__':
    main()
