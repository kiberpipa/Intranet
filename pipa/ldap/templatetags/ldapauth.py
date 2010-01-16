
from django import forms
from django.core.urlresolvers import reverse
from django.template import Node, Context, Library, loader
from pipa.ldap.forms import LDAPPasswordChangeForm

register = Library()

class LDAPPasswordChangeNode(Node):
	def __init__(self):
		pass
	
	def render(self, context):
		t = loader.get_template('ldap/password_change_node.html')
		if not context.get('ldap_password_change_form', None):
			context['ldap_password_change_form'] = LDAPPasswordChangeForm()
		context['ldap_password_change_url'] = reverse('ldap_password_change')
		return t.render(context)

def ldap_password_change(parser, token):
	return LDAPPasswordChangeNode()

ldap_password_change = register.tag('ldap_password_change', ldap_password_change)
