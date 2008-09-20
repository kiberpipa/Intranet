import ldap

from django.contrib.auth.models import User
from django.conf import settings

from intranet.org.models import UserProfile


class backend:
    ##return None if the username/password don't match or needed attributes if they do
    def auth(self, username, password):
        ##define some vars we gonna use in this function
        base = "dc=kiberpipa,dc=org"
        user = 'uid=%s,ou=people,dc=kiberpipa,dc=org' % username
        filter = "(&(objectclass=intranet)(uid=%s))" % username
        ret = ['dn']
        
        l = ldap.initialize(settings.LDAP_SERVER)

        ##step 1: make sure that the user matching the filter actually exists
        try:
            result_id = l.search(base, ldap.SCOPE_SUBTREE, filter, ret)
            result_type, result_data = l.result(result_id, 0)
        except ldap.SERVER_DOWN:
            return None

        if not result_data:
            return None
            
        try:
            l.simple_bind_s(user, password)
            ##if the exception hasn't been raised so far it means the authorization succeded
            return result_data

        except ldap.INVALID_CREDENTIALS:
            return None


    def authenticate(self, username=None, password=None):
        ##make sure the user is authorized
        params = self.auth(username, password)
        if params == None:
            return None

        #create User from ldap credentials if it doesn't exist
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
        
        #insert any ldap logic here
        user.set_password(password)
        user.save()

        try:
            UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=user)
            profile.save()
        
        return user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
