#!/usr/bin/env python
# -*- coding: utf-8 -*
import web
from web import form
import ldap

render = web.template.render('templates/')



urls = (
    '/', 'index'
)

app = web.application(urls, globals())

passform = form.Form(
	form.Password('password'),
	form.Button('OK')
)
search = form.Form(
       	form.Textbox('Email'),
       	form.Button('Ok')
)


class index:
    def POST(self):
	data=web.input(Email='',password='');

	ldapcon = ldap.initialize('ldap://ldapk5.tu-bs.de')
	basedn = 'dc=tu-bs,dc=de'
	searchScope = ldap.SCOPE_SUBTREE
	searchAttribute = ['uid','name', 'ou', 'sn', 'mail', ]
	form = search()
	searchFilter = '(|(uid=*' + data.Email + '*)(mail=*' + data.Email+'*))'
	result_set = []

	if data.password!='ldap4clevershit@tubs' and data.Email=='':
		return render.formres(form,result_set)
	
		
	
	#Bind to the server
	try:
		ldapcon.protocol_version = ldap.VERSION3
		ldapcon.simple_bind_s()
	except ldap.INVALID_CREDENTIALS:
		print "Your username or password is incorrect."
  		sys.exit(0)
	except ldap.LDAPError, e:
  		if type(e.message) == dict and e.message.has_key('desc'):
     			 print e.message['desc']
		else: 
      			print e
  		sys.exit(0)
	try:    
		ldap_result_id = ldapcon.search(basedn, searchScope, searchFilter, searchAttribute)
    		while 1:
        		result_type, result_data = ldapcon.result(ldap_result_id, 0)
       			if (result_data == []):
            			break
        		else:
            			## if you are expecting multiple results you can append them
         			## otherwise you can just wait until the initial result and break out
            			if result_type == ldap.RES_SEARCH_ENTRY:
 		               		result_set.append(result_data)
	except ldap.LDAPError, e:
    		print e
	ldapcon.unbind();
	return render.formres(form,result_set)

    def GET(self):
	form = passform();
	return render.formpass(form)

if __name__ == "__main__":
    #web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
    app.run()
    application = app.wsgifunc()
