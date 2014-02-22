#!/usr/bin/python
import os
import sys

import MySQLdb

import conf.conf as my_conf

def init_database():
    """ This is for the database initialization.
        It will create the tables.
        table UserInfo includes (UserID, UserName, Password, E-mail, \
                SessionID, AccessedTime)
        table SysInfo includes (UserCount, Admin, Admin E-mail, Version)
    """
    try:
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cur = mysql_connect.cursor()
        createUserInfo = """create table UserInfo (
            UserID int primary key,
            UserName varchar(50),
            Password varchar(30),
            EMail varchar(50),
            SessionID varchar(20),
            AccessTime datetime
        );"""
        createSysInfo = """create table SysInfo (
            UserCount int,
            Admin varchar(50),
            AdminEMail varchar(50),
            Ver varchar(20)
        );"""
        try:
            cur.execute(createUserInfo)
            cur.execute(createSysInfo)
            mysql_connect.commit()
        except Exception, e:
            print e
            mysql_connect.rollback()
            return 1
    except Exception, e:
        print e
        return 1
    finally:
        cur.close()
        mysql_connect.close()
    return 0

if __name__ == '__main__':
    if init_database():
        print "init database failed, please check the mysql config"
        sys.exit(1)
    else:
        print "init database ok."
