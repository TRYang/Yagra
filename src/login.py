#!/usr/bin/python
import cgi
import cgitb
import Cookie
import sha
import datetime

import MySQLdb

import conf as my_conf
import mymod.cgifunc as my_cgifunc

cgitb.enable(display=0, logdir=my_conf.CGI_log_dir)

def main():
    #get the form data and get cookies
    form = cgi.FieldStorage()
    if "UserName" not in form or "UserPassword" not in form:
        # The UserName or UserPassword is not finished.
        # Output an error html and a button back to login html
        my_cgifunc.output_error(message='UserName or UserPassword is empty',
                                back_page='back_to_login.py')
    else:
        # fetch password from database, check the sercurity
        mysql_connect = MySQLdb.connect(host=my_conf.mysql_server,
                user=my_conf.mysql_user,
                passwd=my_conf.mysql_password,
                db=my_conf.mysql_database)
        cursor = mysql_connect.cursor()
        try:
            # find user profile in Cache
            command = """select * from Cache
                    where UserName = '%s' or EMail = '%s';""" % (
                            form['UserName'].value, form['UserName'].value)
            cursor.execute(command)
            result = cursor.fetchone()
            # find user profile in UserInfo
            if not result:
                command = """select * from UserInfo
                        where UserName = '%s' or EMail = '%s';""" % (
                                form['UserName'].value, form['UserName'].value)
                cursor.execute(command)
                result = cursor.fetchone()
                hit_cache = 0
            else:
                hit_cache = 1
            cursor.close()
            if not result:
                raise Exception('UserName wrong!')
            password = sha.new(form['UserPassword'].value + result[5])
            if result[2] == password.hexdigest():
                # The UserName and UserPassword is matched
                # set the cookie and return the personal page
                cookie = Cookie.SimpleCookie()
                cookie['sid'] = result[4]
                cookie['sid']['expires'] = 30 * 24 * 60 * 60
                cookie['user'] = result[1]
                cookie['userid'] = str(result[0])
                # Update cache, use LRU(Least Recent Use) algorithm
                cursor = mysql_connect.cursor()
                if hit_cache:
                    #Update cache
                    cursor.execute("""update Cache set UpdateTime = '%s'
                                    where UserID = %d""" % (
                                datetime.datetime.today(), int(result[0])))
                    mysql_connect.commit()
                else:
                    #Insert into cache
                    cursor.execute("""select COUNT(*) from Cache""")
                    cache_count = int(cursor.fetchone()[0])
                    if cache_count == my_conf.Cache_size:
                        # delete one row
                        cursor.execute("""select UserID from Cache
                                where UpdateTime = (
                                select MIN(UpdateTime) from Cache);""")
                        del_id = int(cursor.fetchall()[0][0])
                        cursor.execute("""delete from Cache
                                where UserID = %d""" % del_id)
                    cursor.execute("""insert into Cache (
                    UserID, UserName, Password, EMail, SessionID,
                    Salt, UpdateTime
                    ) values (
                    %d, '%s', '%s', '%s', '%s', '%s', '%s'
                    )""" % (
                    int(result[0]), result[1], result[2], result[3],
                    result[4], result[5], datetime.datetime.today()
                    )
                    )
                    mysql_connect.commit()
                print cookie
                print 'Location: index.py'
                print
            else:
                raise Exception('UserPassword wrong!')
        except Exception, e:
            my_cgifunc.output_error(message=repr(e),
                                    back_page='back_to_login.py'
                                    )
        finally:
            mysql_connect.close()

if __name__ == '__main__':
    main()
