#!/usr/bin/python
import os
import sys
import cgi
import cgitb
import Cookie
import sha
import random

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display = 0, logdir = my_conf.CGI_log_dir)

def gen_sid():
    sid = sha.new()
    sid.update(str(random.random()))
    return sid.hexdigest()

def main():
    form = cgi.FieldStorage()
    # check the form data
    if 'UserName' in form and \
        'UserPassword' in form and \
        'PasswordAgain' in form and \
        'EMail' in form and \
        form['UserPassword'].value == form['PasswordAgain'].value:
        try:
            # insert data into the database
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            cursor = mysql_connect.cursor()
            # check the username and email
            command = """select * from UserInfo
                        where UserName = '%s' or EMail = '%s';""" % (
                        form['UserName'].value,
                        form['EMail'].value
                        )
            cursor.execute(command)
            result = cursor.fetchall()
            # 'nobody' is not available
            if not result and not form['UserName'].value == 'nobody':
                sid = gen_sid()
                cursor.execute('select NextID from SysInfo')
                userid = int(cursor.fetchone()[0])
                password = sha.new(form['UserPassword'].value)
                # insert user information into database
                ins_command = """insert into UserInfo
                    (UserID, UserName, Password, EMail, SessionID) values
                    (%d, '%s', '%s', '%s', '%s')""" % (
                    userid,
                    form['UserName'].value,
                    password.hexdigest(),
                    form['EMail'].value,
                    sid
                    )
                # update system's information
                upd_command1 = """update SysInfo set UserCount = UserCount + 1"""
                upd_command2 = """update SysInfo set NextID = NextID + 1"""
                try:
                    cursor.execute(ins_command)
                    cursor.execute(upd_command1)
                    cursor.execute(upd_command2)
                    mysql_connect.commit()
                except Exception, e:
                    mysql_connect.rollback()
                    my_cgifunc.output_error(
                            message=repr(e),
                            back_page='back_to_register.py'
                            )
                    return
                # set cookie
                cookie = Cookie.SimpleCookie()
                cookie['sid'] = sid
                cookie['sid']['expires'] = 30 * 24 * 60 * 60
                cookie['user'] = form['UserName'].value
                print cookie
                print 'Location: index.py'
                print
            else:
                # username or email had been used
                my_cgifunc.output_error(
                        message='username or email is unavailable',
                        back_page='back_to_register.py'
                        )
        except Exception, e:
            my_cgifunc.output_error(
                    message=repr(e),
                    back_page='back_to_register.py'
                    )
        finally:
            mysql_connect.close()
    else:
        my_cgifunc.output_error(message='register information is not right',
                                back_page='back_to_register.py'
                                )

if __name__ == '__main__':
    main()
