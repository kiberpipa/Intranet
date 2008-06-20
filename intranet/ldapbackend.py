import ldap

from django.contrib.auth.models import User

# Constants
#AUTH_LDAP_SERVER = 'stream.kiberpipa.org'
AUTH_LDAP_SERVER = 'localhost'
#AUTH_LDAP_BASE_USER = "cn=Your, o=BaseUser"
#AUTH_LDAP_BASE_PASS = "Your Base Password"

class backend:
    ##return None if the username/password don't match or needed attributes if they do
    def auth(self, username, password):
        ##define some vars we gonna use in this function
        base = "dc=kiberpipa,dc=org"
        #scope = ldap.SCOPE_SUBTREE
        user = 'uid=%s,ou=people,dc=kiberpipa,dc=org' % username
        filter = "(&(objectclass=jon)(uid=%s))" % username
        ret = ['dn']
        
        l = ldap.open(AUTH_LDAP_SERVER)
        #print filter

        ##step 1: make sure that the user matching the filter actually exists
        result_id = l.search(base, ldap.SCOPE_SUBTREE, filter, ret)
        result_type, result_data = l.result(result_id, 0)
        #print result_data
        
        ##make sure that the user satisfying our filter actually exists
        if not result_data:
            return None
            
        ##verify his/her password
        try:
##            print user
##            print password
            _ = l.simple_bind_s(user, password)
            ##if the exception hasn't been raised so far it means the authorization succeded
            #return User.objects.get(username__exact=username)
            return result_data

        except ldap.INVALID_CREDENTIALS:
            return None


    def luser(self, username, password):
#        user = User(username=username, password="get from ldap") 
        return User(username=username, password=password, user_id=username)
    def authenticate(self, username=None, password=None):
        print "authenticate"
        ##make sure the user is authorized
        params = self.auth(username, password)
        if params == None:
            return None

        ###print "b00"
        #print self.luser(username, password)
        ###User(username=username, password=password)
        return User(username=username, password=password)
#        print "i"
#        print i
        #return self.luser(username, password)









#        ##define some vars we gonna use in this function
#        base = "dc=kiberpipa,dc=org"
#        #scope = ldap.SCOPE_SUBTREE
#        user = 'uid=%s,ou=people,dc=kiberpipa,dc=org' % username
#        filter = "(&(objectclass=jon)(uid=%s))" % username
#        ret = ['dn']
#        
#        l = ldap.open(AUTH_LDAP_SERVER)
#        #print filter
#
#        ##step 1: make sure that the user matching the filter actually exists
#        result_id = l.search(base, ldap.SCOPE_SUBTREE, filter, ret)
#        result_type, result_data = l.result(result_id, 0)
#        #print result_data
#        
#        ##make sure that the user satisfying our filter actually exists
#        if not result_data:
#            return None
#            
#        ##verify his/her password
#        try:
###            print user
###            print password
#            _ = l.simple_bind_s(user, password)
#            ##if the exception hasn't been raised so far it means the authorization succeded
#            return User.objects.get(username__exact=username)
#
#        except ldap.INVALID_CREDENTIALS:
#            return None
        

    def get_user(self, user_id):
        #print "get_user"
        #print user_id
        try:
         #   User.objects.get(pk=user_id)
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

        
##        # Authenticate the base user so we can search
##        try:
##            l = ldap.open(AUTH_LDAP_SERVER)
##            l.protocol_version = ldap.VERSION3
##            l.simple_bind_s(AUTH_LDAP_BASE_USER,AUTH_LDAP_BASE_PASS)
##        except ldap.LDAPError:
##            return None
##
##        try:
##            result_id = l.search(base, scope, filter, ret)
##            result_type, result_data = l.result(result_id, 0)
##
##            # If the user does not exist in LDAP, Fail.
##            if (len(result_data) != 1):
##                return None
##
##            # Attempt to bind to the user's DN
##            l.simple_bind_s(result_data[0][0],password)
##
##            # The user existed and authenticated. Get the user
##            # record or create one with no privileges.
##            try:
##                user = User.objects.get(username__exact=username)
##            except:
##                # Theoretical backdoor could be input right here. We don't
##                # want that, so input an unused random password here.
##                # The reason this is a backdoor is because we create a
##                # User object for LDAP users so we can get permissions,
##                # however we -don't- want them able to login without
##                # going through LDAP with this user. So we effectively
##                # disable their non-LDAP login ability by setting it to a
##                # random password that is not given to them. In this way,
##                # static users that don't go through ldap can still login
##                # properly, and LDAP users still have a User object.
##                from random import choice
##                import string
##                temp_pass = ""
##                for i in range(8):
##                    temp_pass = temp_pass + choice(string.letters)
##                user = User.objects.create_user(username,
##                         username + '@carthage.edu',temp_pass)
##                user.is_staff = False
##                user.save()
##            # Success.
##            return user
##           
##        except ldap.INVALID_CREDENTIALS:
##            # Name or password were bad. Fail.
##            return None

