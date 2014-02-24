#!/usr/bin/python
import cgi
import cgitb
import Cookie

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display = 0, logdir = my_conf.CGI_log_dir)

def main():
    # clear the cookie and return the index.html
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie['sid'] = ""
    cookie['user'] = 'nobody'
    print cookie
    print 'Location: index.py'
    print

if __name__ == '__main__':
    main()
