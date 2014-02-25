INSTALL_PATH = /home/apache
DOC = doc/index.html doc/login.html doc/register.html doc/reset_password.html
CONF = conf/conf.py
SCRIPT = src/index.py src/login.py src/back_to_login.py src/showPage.py \
		  src/register.py src/back_to_register.py src/logout.py src/upload.py \
		  src/reset.py
MOD = mymod

all: $(DOC) $(SCRIPT)
	cp $(DOC) $(INSTALL_PATH)/doc/
	cp $(CONF) $(INSTALL_PATH)/cgi-bin/
	cp $(SCRIPT) $(INSTALL_PATH)/cgi-bin/
	cp src/$(MOD)/* $(INSTALL_PATH)/cgi-bin/$(MOD)/
