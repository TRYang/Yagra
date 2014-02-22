#!/usr/bin/python
import cgi
import cgitb
import Cookie

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display = 0, logdir = my_conf.CGI_log_dir)

def output_error():
    """ Output an error html
    """
    print my_cgifunc.content_type()
    print """<HTML><HEAD><TITLE>Error</TITLE></HEAD>
             <BODY><H1>UserName or Password error!</H1><br/>
             Click back to login page : %s</BODY></HTML>""" %\
             my_cgifunc.back_button()

def output_error2():
    """ Output an error html
    """
    print my_cgifunc.content_type()
    print """<HTML><HEAD><TITLE>Error!!!!!!!!</TITLE></HEAD>
             <BODY><H1>UserName or Password error!</H1><br/>
             Click back to login page : %s</BODY></HTML>""" %\
             my_cgifunc.back_button()

def main():
    #get the form data and get cookies
    form = cgi.FieldStorage()
    if "UserName" not in form or "UserPassword" not in form:
        # The UserName or UserPassword is not finished.
        # Output an error html and a button back to login html
        output_error()
    else:
        # fetch password from database, check the sercurity
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cursor = mysql_connect.cursor()
        try:
            command = """select * from UserInfo
                    where UserName = '%s';""" % form['UserName'].value
            cursor.execute(command)
            result = cursor.fetchone()
            cursor.close()
            if not result:
                raise Exception
            if result[2] == form['UserPassword'].value:
                # The UserName and UserPassword is matched
                # set the cookie and return the personal page
                cookie = Cookie.SimpleCookie()
                cookie['sid'] = result[4]
                cookie['sid']['expires'] = 30 * 24 * 60 * 60
                cookie['user'] = form['UserName'].value
                print cookie
                print 'Location: showPage.py'
                print
            else:
                output_error()
                #raise Exception
        except Exception, e:
            #output_error()
            print my_cgifunc.content_type()
            print my_cgifunc.html_header()
            print command
            print e
            print my_cgifunc.html_tail()
        finally:
            mysql_connect.close()

if __name__ == '__main__':
    main()
