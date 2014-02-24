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
            创建用户：create 'user_name'@'server_address' identified by 'user_password';
            创建数据库：create database 'database_name';
            授权：grant all on 'database_name'.* to 'user_name';

    2、配置管理员信息
        AdminName：管理员姓名或id
        AdminEMail：管理员的E-mail地址，用于系统故障发送报告到邮箱

    3、配置服务器信息
        DocPath：服务器存放文档的根目录
        CgiPath：服务器存放cgi程序的目录

4. 待完善地方
    
    1、现在密码是明文保存，需改进
    2、登录只能使用用户名，改成可使用用户名或邮箱
    3、目前用户名的字符集没有限定，应限定
