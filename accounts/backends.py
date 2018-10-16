from django.contrib.auth.models import User

class EmailAuth:
    # authenticate a user based on email provided
    
    def authenticate(self, username=None, password=None):
    
    # get an instance of the user based off the email and verify the pasword
    
        try:
            user = User.objects.get(email=username)
            
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        # user by the django auth system to retrieve a user instance
        
        try:
            user = User.objects.get(pk=user_id)
            
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None