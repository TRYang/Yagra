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
    # check the form data
    mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
            user=my_conf.mysql_user,
            passwd=my_conf.mysql_password,
            db=my_conf.mysql_database)

if __name__ == '__main__':
    main()
