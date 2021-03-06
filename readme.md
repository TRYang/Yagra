1.功能需求：

    要求建立一个完整的站点，详细功能要求如下：

    1、注册（用户名，密码；用户名不一定要求是邮箱，你可以自己定规则）
    2、登录，登出
    3、上传头像（只需要一个头像即可，但是要求可以替换，不需要头像编辑等功能）
    4、提供头像访问API（无需支持size、default等参数，只要求能访问原图即可）

2.设计方案：

    源码分三类：静态文件，cgi程序，配置文件

    静态文件：
        主页
        登录界面
        注册界面
        找回密码界面
        重置密码界面
        API使用文档界面
    cgi程序：
        索引，用于判断cookie直接登录（index.py）
        注册（register.py）
        登录（login.py）
        登出（logout.py）
        上传头像（upload.py）
        修改密码（reset.py）
        根据用户id显示用户的主页（showPage.py）
        找回密码（findout.py）*
    配置文件：
        由于所有程序采用python开发，配置文件也是用python格式，方便引用。
        需要配置的项在安装说明中说明。
    安装程序：
        setup.py  功能是初始化数据库，还有一些出错情况没处理完
    头像文件：
        用户的头像文件，直接存放在http服务器下，将路径信息存入数据库
    密码：
        密码保存的方式时在明文后添加一段salt，再用sha-1算法加密，最后得到40位长的16进制串
        可以通过注册用的邮箱找回密码，采用smtplib发邮件给用户进行重设密码
    用户名：
        可使用用户名或邮箱进行登录
    邮箱：
        每个帐号都必须绑定一个唯一的邮箱，不能有两个不同的UserName绑定到同一个邮箱
        邮箱名可以作为用户名登录
        当忘记密码后也可以让系统发一个修改密码的邮件到绑定的邮箱
        用户随时可以改变绑定的邮箱，但必须保证唯一性
    API:
        可用http://server_address/data/finger来获取用户user_name的头像
        finger采用sha算法进行hash，python可以用一下代码获取指纹：
            import sha
            print sha.new(user_name).hexdigest()
        例如服务器的域名是localhost，用户名为'test'
        则可以用一下的url获取头像：
            http://localhost/data/a94a8fe5ccb19ba61c4c0873d391e987982fbbd3
    Cache:
        增加了Cache功能，在用户登录时进行优化，根据用户上次登录的时间，cache最近登录过的用户。
        当用户数量巨大时，用户登录会先查询cache table，如果最近登录过，则很快可以获得登录信息。


    站点实现主要通过cgi程序，调用mysql接口，实现数据（头像）的上传和下载。
    用户的功能通过http的session来实现，通过读取cookie中的sid和设置来判断用户。

    带*号项为扩展，可选实现

3.安装说明：

    1、配置mysql
        首先需要配置conf/conf.py中的mysql服务器信息
            mysql_server：mysql服务器的地址
            mysql_user：登录mysql的用户
            mysql_password：登录mysql用户对应的密码
            mysql_database：mysql使用的database
        配置完后需要用mysql管理员创建mysql_user用户，创建mysql_database，授权给用户。
            创建用户：create user 'user_name'@'server_address' identified by 'user_password';
            创建数据库：create database 'database_name';
            授权：grant all on 'database_name'.* to 'user_name';

    2、配置管理员信息
        AdminName：管理员姓名或id
        AdminEMail：管理员的E-mail地址，用于系统故障发送报告到邮箱

    3、配置服务器信息
        http_doc_path：服务器存放文档的根目录
        http_cgi_path：服务器/cgi-bin/的目录
        * 以上两项根据http server的配置文件来设置
        * 注意目录的权限问题，必须具有写权限。
        CGI_log_dir：服务器存放cgi程序日志的目录

    4、配置管理邮箱信息
        Server_mail：管理用的邮箱名，用于发邮件帮助用户找回丢失的密码
        Server_mail_host：邮箱服务器的域名
        Server_mail_password：登录邮箱的密码
        Server_mail_postfix：邮箱地址的后缀

    5、运行脚本
        配置好参数后，执行一下命令：
            ./setup.py init

