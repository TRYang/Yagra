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

    print my_cgifunc.content_type()
    print """<HTML><HEAD>hello</HEAD><BODY>%s</BODY></HTML>""" % cookie['user'].value

if __name__ == '__main__':
    main()
