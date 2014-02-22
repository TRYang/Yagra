#!/usr/bin/python

def content_type(ctype = 'text/html'):
  return 'Content-Type: %s\n\n' % ctype

def html_header(title = "cgi-response"):
  return """<html>
<head>
<title>%s</title>
</head>
<body>""" % title

def html_tail():
  return '</body></html>'

def back_button():
    return """<FORM METHOD=GET ACTION=back_to_login.py>
  <INPUT TYPE="SUBMIT" VALUE="BACK" NAME="Back">
  </FORM>"""

def link(url):
    print content_type()
    print """
        <HTML>
        <head>
        <meta http-equiv="Refresh" content="0;URL=%s">
        </head>
        <body>
        </body>
        </HTML>
        """ % url
