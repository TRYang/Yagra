#!/usr/bin/python
import os
import cgi
import cgitb
import sys
import fileinput
import Cookie
import random
import sha
import os.path
import datetime

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display = 0, logdir = my_conf.CGI_log_dir)

def main():
    # get the form data
    form = cgi.FieldStorage()
    cookie = Cookie.SimpleCookie()
    cookie.load(os.environ.get('HTTP_COOKIE'))
    # check the file type
    if form['file'].filename.split('.')[-1].lower() in ['jpg', 'gif', 'png']:
        user = cookie['user'].value
        file_path = ""
        # get the user's avatar from mysql
        try:
            mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                    user=my_conf.mysql_user,
                    passwd=my_conf.mysql_password,
                    db=my_conf.mysql_database)
            cursor = mysql_connect.cursor()
            cursor.execute("""select * from UserPath where UserID = %d;""" %
                            int(cookie['userid'].value))
            result = cursor.fetchone()
            if result[1]:
                os.remove(os.path.join(my_conf.http_doc_path + my_conf.DataPath,
                            result[1]))
            filename = sha.new(cookie['user'].value).hexdigest()
            file_path = os.path.join(my_conf.http_doc_path + my_conf.DataPath,
                                    filename)
            with open(file_path, 'w+b') as fp:
                fp.write(form['file'].file.read())
            cur_datetime = datetime.datetime.today()
            cursor.execute("""update UserPath set Path = '%s',
                            UpdateTime = '%s'
                            where UserID = %d;""" % (
                            filename,
                            cur_datetime,
                            int(cookie['userid'].value))
                        )
            mysql_connect.commit()
            cursor.close()
            print my_cgifunc.content_type()
            print my_cgifunc.html_header("upload success")
            print '<h1>upload your new avatar successful!!!</h1>'
            print """<form method=get action=/cgi-bin/showPage.py>
                    <input type=submit value="Back">
                    </form>"""
            print my_cgifunc.html_tail()
        except Exception, e:
            print my_cgifunc.content_type()
            print my_cgifunc.html_header('Upload error')
            print '<h1>%s</h1>' % file_path
            print '<h3>Error : %s</h3>' % repr(e)
            print """<form method=get action=showPage.py>
                    <input type=submit value="Back">
                    </form>"""
            print my_cgifunc.html_tail()
        finally:
            mysql_connect.close()


    else:
        print my_cgifunc.content_type()
        print my_cgifunc.html_header('Upload error')
        print '<h2>The file is not a (.jpg, .gif, .png) file</h2>'
        print """<form method=get action=showPage.py>
                <input type=submit value="Back">
                </form>"""
        print my_cgifunc.html_tail()

if __name__ == '__main__':
    main()
