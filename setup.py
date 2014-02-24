#!/usr/bin/python
import os
import sys

import MySQLdb

import conf.conf as my_conf

def usage():
    print "Usage: ./%s command" % sys.argv[0]
    print """command:
    init        # the first step to init the database and others
    reset       # to clear all the data"""

def init_database():
    """ This is for the database initialization.
        It will create the tables.
        table UserInfo includes (UserID, UserName, Password, E-mail, \
                SessionID)
        table SysInfo includes (UserCount, Admin, Admin E-mail, Version)

        And store the system information into the database.
    """
    try:
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cur = mysql_connect.cursor()
        createUserInfo = """create table UserInfo (
            UserID int primary key,
            UserName varchar(%d),
            Password varchar(%d),
            EMail varchar(%d),
            SessionID char(%d)
        );""" % (my_conf.UserName_length,
                my_conf.Password_length,
                my_conf.EMail_length,
                my_conf.SessionID_length)

        createSysInfo = """create table SysInfo (
            UserCount int,
            Admin varchar(50),
            AdminEMail varchar(50),
            Ver varchar(20),
            NextID int
        );"""
        insertSysInfo = """insert into SysInfo(
        UserCount, Admin, AdminEMail, Ver, NextID) values (
        0, '%s', '%s', '%s', 1)""" % (
                my_conf.AdminName,
                my_conf.AdminEMail,
                my_conf.Version)
        try:
            cur.execute(createUserInfo)
            cur.execute(createSysInfo)
            cur.execute(insertSysInfo)
            mysql_connect.commit()
        except Exception, e:
            print e
            cur.close()
            mysql_connect.rollback()
            return 1
        cur.close()
    except Exception, e:
        print e
        return 1
    finally:
        mysql_connect.close()
    return 0

def drop_database():
    """This function is for clear all data in database.
        Sometime this is useful for testing or the user want
        to uninstall the website
    """
    try:
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cur = mysql_connect.cursor()
        dropUserInfo = """drop table UserInfo;"""
        dropSysInfo = """drop table SysInfo;"""
        try:
            cur.execute(dropUserInfo)
            cur.execute(dropSysInfo)
            mysql_connect.commit()
        except Exception, e:
            mysql_connect.rollback()
            print e
            return 1
        cur.close()
    except Exception, e:
        print e
        return 1
    finally:
        mysql_connect.close()
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    if sys.argv[1] == 'init':
        if init_database():
            print "init database failed, please check the mysql config"
            sys.exit(1)
        else:
            print "init database ok."

    elif sys.argv[1] == 'reset':
        if drop_database():
            print "drop database failed, please check the mysql"
            sys.exit(1)
        else:
            print "drop database ok."
