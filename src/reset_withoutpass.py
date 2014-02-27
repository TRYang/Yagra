#!/usr/bin/python
# coding: UTF-8
import cgi
import cgitb
import sha

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def main():
    form = cgi.FieldStorage()
    if 'new_password' in form and \
        'password_again' in form and \
        form['new_password'].value == form['password_again'].value:
        try:
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            cursor = mysql_connect.cursor()
            cursor.execute("""select * from UserInfo
                        where UserID = %d;""" % int(form['UserID'].value))
            result = cursor.fetchone()
            if not result:
                raise Exception("Connect to database error!")
            if result[2] == form['Finger'].value:
                salt = result[5]
                password = sha.new(form['new_password'].value+salt).hexdigest()
                cursor.execute("""update UserInfo set Password = '%s'
                                where UserID = %d;""" % (
                                password,
                                int(form['UserID'].value)
                                )
                            )
                cursor.execute("""update Cache set Password = '%s'
                                where UserID = %d;""" % (
                                password,
                                int(form['UserID'].value)
                                )
                            )
            else:
                raise Exception("Findger is not right, contact the admin!")
            cursor.close()
            mysql_connect.commit()
            print my_cgifunc.content_type()
            print my_cgifunc.html_header('Reset password success')
            print """<H1>Reset password ok</h1>
                     <form method=get action=/index.html>
                        <input type=submit value="首页">
                     </form>
                  """
            print my_cgifunc.html_tail()
        except Exception, e:
            my_cgifunc.output_error(
                message=repr(e),
                back_page="/index.html"
            )
        finally:
            mysql_connect.close()
    else:
        my_cgifunc.output_error(
            message="the new password is not right!",
            back_page="/index.html"
            )

if __name__ == '__main__':
    main()
