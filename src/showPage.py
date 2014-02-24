#!/usr/bin/python
# coding: UTF-8
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

def main():
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie_str = os.environ['HTTP_COOKIE']
    cookie.load(cookie_str)

    # print the html header
    print my_cgifunc.content_type()
    print my_cgifunc.html_header(cookie['user'].value)
    # get the user information from database
    mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
            user=my_conf.mysql_user,
            passwd=my_conf.mysql_password,
            db=my_conf.mysql_database)
    cursor = mysql_connect.cursor()
    cursor.execute("select * from UserInfo where UserName = '%s';" %
            cookie['user'].value)
    result = cursor.fetchone()
    cursor.execute("select * from UserPath where UserID = %d;" %
                int(cookie['userid'].value))
    avatar_path = cursor.fetchone()[1]
    cursor.close()
    mysql_connect.close()
    if result:
        print '<H1>UserName : %s</H1>' % result[1]
        print '<h3>UserID : %d</H1>' % result[0]
        print '<h3>User E-mail : %s</h3>' % result[3]
        print '<img src="http://%s:%s/%s/%s" alt="avatar">' % (
                os.environ.get('SERVER_NAME'),
                os.environ.get('SERVER_PORT'),
                my_conf.DataPath,
                avatar_path)
        print '<h3>Session ID(cookie) : %s</h3>' % cookie['sid'].value
        print '<h3>Session ID : %s</h3>' % result[4]
        print '<h3>Password : %s</h3>' % result[2]
        print """<FORM METHOD=POST ENCTYPE="multipart/form-data" \
                action=/cgi-bin/upload.py>
                    <input type=FILE NAME="file">
                    <input type=SUBMIT value="upload" NAME="upload">
                </FORM>
              """
        print """<FORM METHOD=GET ACTION=/cgi-bin/logout.py>
                <INPUT TYPE=SUBMIT VALUE="登出" NAME="Logout">
                </FORM>"""
    else:
        my_cgifunc.output_error(message='login error!',
                                back_page='back_to_login.py')
    # print the html tail
    print my_cgifunc.html_tail()

if __name__ == '__main__':
    main()
