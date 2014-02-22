import sha
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
Password_length = 10
# The maximum length of the E-mail
EMail_length = 30
# The length of the session id
SessionID_length = sha.digest_size

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
# This is log configuration
#====================================================
# The cgi script log dir
CGI_log_dir = '/home/terry/log'
