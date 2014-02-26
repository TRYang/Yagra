#=================================================
# This is the mysql server configuration
#=================================================
# mysql server address
mysql_server = 'localhost'
# mysql user name
mysql_user = 'Yagra'
# mysql user password
mysql_password = 'Yagra'
# mysql database
mysql_database = 'Yagra'

#====================================================
# This is the argument for mysql data
# Don't modify it unless you know what you are doing
#====================================================
# The maximum length of the UserName
UserName_length = 30
# The maximum length of the Password
Password_length = 40
# The maximum length of the E-mail
EMail_length = 50
# The length of the session id
SessionID_length = 40
# The length of salt
Salt_length = 10

#====================================================
# This is the administrator configuration
#====================================================
# The admin name
AdminName = "RuiyangTan"
# The admin email
AdminEMail = "ruiyangtan_terry@163.com"

#====================================================
# This is the version info
#====================================================
# version
Version = "0.1"

#====================================================
# This is http server information
#====================================================
# http document root
http_doc_path = '/home/apache/doc/'
# Document root, relative to http document root
DocPath = '/'
# Cgi script root, relative to http document root
CgiPath = '/cgi-bin/'
# The cgi script log root
CGI_log_dir = '/home/terry/log'
# The data root, relative to http document root
DataPath = '/data/'

#====================================================
# This is the server mail information
#====================================================
# The server mail-box address, use for send mail to user
Server_mail = 'ruiyang_Yagra'
# The server mail-box host
Server_mail_host = 'smtp.163.com'
# The server mail-box password
Server_mail_password = 'forYagra'
# The server mail-box postfix
Server_mail_postfix = '163.com'

