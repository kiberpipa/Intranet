
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

from pipa.ldap.forms import LDAPPasswordChangeForm

def password_change(request):
	
	msg = ''
	pw_form = LDAPPasswordChangeForm()
	
	if request.method == 'POST':
		pw_form = LDAPPasswordChangeForm(request.POST)
		
		if pw_form.is_valid():
			import ldap
			if pw_form.cleaned_data['new_password'] == pw_form.cleaned_data['new_password_confirm']:
				msg = 'Password successfuly set.'
				try:
					l = ldap.initialize(settings.LDAP_SERVER)
					dn = 'uid=%s,ou=people,dc=kiberpipa,dc=org' % request.user.username
					l.simple_bind_s(dn, pw_form.cleaned_data['old_password'])
					l.passwd_s(dn, pw_form.cleaned_data['old_password'], pw_form.cleaned_data['new_password'])
				except ldap.SERVER_DOWN:
					msg = 'LDAP server seems to be unavailable. Better luck next time. OH, and do notify the admins!'
				except ldap.CONSTRAINT_VIOLATION, e:
					msg = e[0]['info']
				except ldap.INVALID_CREDENTIALS:
					msg = 'Sorry, wrong password.'
			else:
				msg = 'Sorry, new password doesn not match the confirm.'
	
	context = {
		'message': msg,
		'ldap_password_change_form': pw_form,
		}
	return render_to_response('ldap/password_change.html', RequestContext(request, context))
