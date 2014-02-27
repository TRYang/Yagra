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

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def main():
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie_str = os.environ['HTTP_COOKIE']
    cookie.load(cookie_str)

    if 'userid' not in cookie or 'user' not in cookie:
        my_cgifunc.output_error(
                message="user information error!",
                back_page="index.py"
                )
        return

    # print the html header
    print my_cgifunc.content_type()
    print my_cgifunc.html_header(cookie['user'].value)
    # get the user information from database
    try:
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cursor = mysql_connect.cursor()
        cursor.execute("""select * from Cache
                        where UserID = %d""" % int(cookie['userid'].value))
        result = cursor.fetchone()
        if not result:
            #not hit cache, get the information from UserInfo
            cursor.execute("""select * from UserInfo
                        where UserID = %d""" % int(cookie['userid'].value))
            result = cursor.fetchone()
    except Exception, e:
        my_cgifunc.output_error(
                message=repr(e),
                back_page="index.py"
                )
        return
    finally:
        mysql_connect.close()
    if result:
        avatar_path = sha.new(result[1]).hexdigest()
        print '<H1>UserName : %s</H1>' % result[1]
        print '<h3>User E-mail : %s</h3>' % result[3]
        if os.path.exists(os.path.join(my_conf.http_doc_path+ '/data/', avatar_path)):
            print '<img src="http://%s:%s/%s/%s" alt="avatar">' % (
                    os.environ.get('SERVER_NAME'),
                    os.environ.get('SERVER_PORT'),
                    'data',
                    avatar_path)
        else:
            print '<h3>You should upload a image as your avatar</h3>'
        print """<FORM METHOD=POST ENCTYPE="multipart/form-data" \
                action=upload.py>
                    <input type=FILE NAME="file">
                    <input type=SUBMIT value="upload" NAME="upload">
                </FORM>
              """
        print """<FORM METHOD=GET ACTION=/reset_password.html>
                <INPUT TYPE=SUBMIT VALUE="修改密码" NAME="Reset">
                </FORM>"""
        print """<FORM METHOD=GET ACTION=logout.py>
                <INPUT TYPE=SUBMIT VALUE="登出" NAME="Logout">
                </FORM>"""
    else:
        my_cgifunc.output_error(message='login error!',
                                back_page='back_to_login.py')
    # print the html tail
    print my_cgifunc.html_tail()

if __name__ == '__main__':
    main()
