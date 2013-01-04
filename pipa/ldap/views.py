import urlparse

import ldap
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, REDIRECT_FIELD_NAME
from django.conf import settings
from django.http import HttpResponseRedirect

from pipa.ldap.forms import LDAPPasswordChangeForm


@login_required
def password_change(request):
    msg = ''
    pw_form = LDAPPasswordChangeForm(request.POST or None)

    if request.POST and pw_form.is_valid():
        new_pass = pw_form.cleaned_data['new_password']
        old_pass = pw_form.cleaned_data['old_password']
        if new_pass == pw_form.cleaned_data['new_password_confirm']:
            msg = 'Password successfuly set.'
            try:
                l = ldap.initialize(settings.LDAP_SERVER)
                dn = 'uid=%s,ou=people,dc=kiberpipa,dc=org' % request.user.username
                l.simple_bind_s(dn, old_pass)
                l.passwd_s(dn, old_pass, new_pass)
            except ldap.CONSTRAINT_VIOLATION, e:
                msg = e[0]['info']
            except ldap.INVALID_CREDENTIALS:
                msg = 'Sorry, wrong password'
        else:
            msg = 'Sorry, passwords do not match'

    return render_to_response("ldap/password_change.html",
                              {'message': msg,
                               'ldap_password_change_form': pw_form},
                              context_instance=RequestContext(request))


def login(request, *args, **kwargs):
    if request.method == 'POST':
        if request.POST.get('remember_me', None) == 'on':
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)

    # if we have next parameter, do redirect
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    if request.method == "GET" and request.user.is_authenticated() and redirect_to:
        return HttpResponseRedirect(redirect_to)

    # hack: django does not allow redirects out of its domain
    if redirect_to:
        def get_host():
            return urlparse.urlparse(redirect_to)[1]
        request.get_host = get_host

    return auth_views.login(request, *args, **kwargs)
