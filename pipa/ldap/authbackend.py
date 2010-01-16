from django.contrib.auth.models import User
from django.conf import settings

from intranet.org.models import UserProfile

ldap = None

class LDAPAuthBackend:
    ##return None if the username/password don't match or needed attributes if they do
    def auth(self, username, password):
        global ldap
        if ldap is None:
            import ldap

        ##define some vars we gonna use in this function
        base = "dc=kiberpipa,dc=org"
        user = 'uid=%s,ou=people,dc=kiberpipa,dc=org' % username.encode('utf-8')
        filter = "(&(objectclass=intranet)(uid=%s))" % username.encode('utf-8')
        ret = ['uid', 'givenName', 'sn']

        l = ldap.initialize(settings.LDAP_SERVER)

        ##step 1: make sure that the user matching the filter actually exists
        try:
            result_id = l.search(base, ldap.SCOPE_SUBTREE, filter, ret)
            result_type, result_data = l.result(result_id, 0)
        except ldap.SERVER_DOWN:
            return None

        if not result_data:
            return None

        #example result_data: [('uid=puffs,ou=People,dc=kiberpipa,dc=org', {'uid': ['puffs']})]
        #compensate for ldap's case insensitivity
        if result_data[0][1]['uid'][0] != username:
            return None

        try:
            l.simple_bind_s(user, password.encode('utf-8'))
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

        # insert any LDAP logic here
        user.set_password(password)
        if not user.first_name:
            user.first_name = params[0][1]['givenName'][0]
        if not user.last_name:
            user.last_name = params[0][1]['sn'][0]
        # if a user still exists in ldap AND tries to log in, should be safe to set the active flag
        user.is_active = True
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
