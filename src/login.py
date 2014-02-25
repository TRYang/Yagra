#!/usr/bin/python
import cgi
import cgitb
import Cookie
import sha

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display = 0, logdir = my_conf.CGI_log_dir)

def main():
    #get the form data and get cookies
    form = cgi.FieldStorage()
    if "UserName" not in form or "UserPassword" not in form:
        # The UserName or UserPassword is not finished.
        # Output an error html and a button back to login html
        my_cgifunc.output_error(message='UserName or UserPassword is empty',
                                back_page='back_to_login.py')
    else:
        # fetch password from database, check the sercurity
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cursor = mysql_connect.cursor()
        try:
            command = """select * from UserInfo
                    where UserName = '%s' or EMail = '%s';""" % (
                            form['UserName'].value, form['UserName'].value)
            cursor.execute(command)
            result = cursor.fetchone()
            cursor.close()
            if not result:
                raise Exception('UserName wrong!')
            password = sha.new(form['UserPassword'].value + result[5])
            if result[2] == password.hexdigest():
                # The UserName and UserPassword is matched
                # set the cookie and return the personal page
                cookie = Cookie.SimpleCookie()
                cookie['sid'] = result[4]
                cookie['sid']['expires'] = 30 * 24 * 60 * 60
                cookie['user'] = result[1]
                cookie['userid'] = str(result[0])
                print cookie
                print 'Location: index.py'
                print
            else:
                raise Exception('UserPassword wrong!')
        except Exception, e:
            my_cgifunc.output_error(message=repr(e),
                                    back_page='back_to_login.py'
                                    )
        finally:
            mysql_connect.close()

if __name__ == '__main__':
    main()
