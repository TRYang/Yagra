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
    cursor.close()
    mysql_connect.close()
    if result:
        print '<H1>UserName : %s</H1>' % result[1]
        print '<h3>User E-mail : %s</h3>' % result[3]
        print '<h3>Session ID : %s</h3>' % cookie['sid'].value
    else:
        my_cgifunc.output_error(message='login error!',
                                back_page='back_to_login.py')
    # print the html tail
    print my_cgifunc.html_tail()

if __name__ == '__main__':
    main()
