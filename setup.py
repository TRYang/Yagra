#!/usr/bin/python
import os
import sys
import os.path
import shutil

import MySQLdb

import conf.conf as my_conf

# myself module list
mod_list = ['src/mymod']

def usage():
    print "Usage: ./%s command" % sys.argv[0]
    print """command:
    init        # the first step to init the database and others
    reset       # to clear all the data"""

def init_database():
    """ This is for the database initialization.
        It will create the tables.
        table UserInfo includes (UserID, UserName, Password, E-mail, \
                SessionID, Salt)
        table UserPath includes (UserID, Path, UpdateTime)
        table SysInfo includes (UserCount, Admin, Admin E-mail, Version)
        table Cache includes (UserID, UserName, Password, E-mail, \
                SessionID, Salt, UpdateTime)

        And store the system information into the database.
    """
    try:
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cur = mysql_connect.cursor()
        dropUserInfo = """drop table if exists UserInfo;"""
        dropUserPath = """drop table if exists UserPath;"""
        dropSysInfo = """drop table if exists SysInfo;"""
        dropCache = """drop table if exists Cache;"""
        createUserInfo = """create table UserInfo (
            UserID int primary key,
            UserName varchar(%d),
            Password varchar(%d),
            EMail varchar(%d),
            SessionID char(%d),
            Salt char(%d)
        );""" % (my_conf.UserName_length,
                my_conf.Password_length,
                my_conf.EMail_length,
                my_conf.SessionID_length,
                my_conf.Salt_length)
        createCache = """create table Cache (
            UserID int primary key,
            UserName varchar(%d),
            Password varchar(%d),
            EMail varchar(%d),
            SessionID char(%d),
            Salt char(%d),
            UpdateTime datetime
        );""" % (my_conf.UserName_length,
                my_conf.Password_length,
                my_conf.EMail_length,
                my_conf.SessionID_length,
                my_conf.Salt_length)
        createUserPath = """create table UserPath (
            UserID int,
            Path varchar(100),
            UpdateTime datetime
            );"""
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
            cur.execute(dropUserInfo)
            cur.execute(dropCache)
            cur.execute(dropUserPath)
            cur.execute(dropSysInfo)
            cur.execute(createUserInfo)
            cur.execute(createCache)
            cur.execute(createUserPath)
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
        dropUserInfo = """drop table if exists UserInfo;"""
        dropCache = """drop table if exists Cache;"""
        dropUserPath = """drop table if exists UserPath;"""
        dropSysInfo = """drop table if exists SysInfo;"""
        try:
            cur.execute(dropUserInfo)
            cur.execute(dropCache)
            cur.execute(dropUserPath)
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

def copy_files():
    docs = os.listdir('doc')
    srcs = os.listdir('src')
    confs = os.listdir('conf')
    if not my_conf.http_doc_path or \
        not os.path.isdir(my_conf.http_doc_path):
        print "Http doc path '%s' is not exists." % my_conf.http_doc_path
        return 1
    if not my_conf.http_cgi_path or \
        not os.path.isdir(my_conf.http_cgi_path):
        print "Http cgi-bin path '%s' is not exists." % my_conf.http_cgi_path
        return 1
    if not os.path.isdir(os.path.join(
        my_conf.http_doc_path, 'data')):
        os.mkdir(os.path.join(my_conf.http_doc_path, 'data'))
    for doc in docs:
        shutil.copy(os.path.join('doc/', doc), my_conf.http_doc_path)
    for src in srcs:
        if os.path.isfile(os.path.join('src/', src)):
            shutil.copy(os.path.join('src/', src), my_conf.http_cgi_path)
    for conf in confs:
        shutil.copy(os.path.join('conf/', conf), my_conf.http_cgi_path)
    for mod in mod_list:
        shutil.copytree(mod, os.path.join(
                    my_conf.http_cgi_path,
                    mod.split('/')[-1]))
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    if sys.argv[1] == 'init':
        # init database
        if init_database():
            print "init database failed, please check the mysql config"
            sys.exit(1)
        else:
            print "init database ok."

        #copy the file to the server root
        if copy_files():
            print "copy files failed, please check the Path configuration in the 'conf/conf.py'"
            sys.exit(1)
        else:
            print "copy files ok."

    elif sys.argv[1] == 'reset':
        if drop_database():
            print "drop database failed, please check the mysql"
            sys.exit(1)
        else:
            print "drop database ok."
