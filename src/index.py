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

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def main():
    #get the form data and get cookies
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie_str = os.environ.get('HTTP_COOKIE')

    # check if cookie exist
    if not cookie_str:
        # This is a new session.
        # Relocate to login.html
        my_cgifunc.link('/login.html')
    else:
        # The session is already exist
        # identify the UserName in cookies
        cookie.load(cookie_str)
        if 'user' not in cookie or cookie['user'].value == 'nobody':
            my_cgifunc.link('/login.html')
            return
        sid = cookie['sid'].value
        # select username and session id from database
        # and compare with the session id from cookie
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cur = mysql_connect.cursor()
        cur.execute("""select UserID
                     from UserInfo
                     where UserID = %d and SessionID = '%s';""" %
                     (int(cookie['userid'].value), sid))
        result = cur.fetchone()
        cur.close()
        mysql_connect.close()
        # according to the result selected from database
        if result:
            print cookie
            print 'Location: showPage.py'
            print
        else:
            my_cgifunc.link('/login.html')

if __name__ == '__main__':
    main()
