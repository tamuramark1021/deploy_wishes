from django.db import models
import bcrypt     # support for password hashing
import re         # support for regular expressions

EMAIL_REG = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    # validating the user inputs for the registration page
    def validate(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First name must be at least 3 characters"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last name must be at least 3 characters"
        if not EMAIL_REG.match(post_data['email']):
            errors['email'] = "Email address is not valid"
        if len(post_data['password']) < 8:
            errors['password'] = "Passwords must be at least 8 characters"
        if post_data['confirm_pw'] != post_data['password']:
            errors['confirm'] = "Passwords do not match"
        return errors
    
    # this is ONLY called AFTER we have validated the inputs for registration
    def register(self, post_data):
        # create a hashed password to be saved in the DB
        #   be VERY careful with parenthesis and to .decode() at the end before saving to the DB
        hashed_pw = bcrypt.hashpw(post_data['password'].encode(), bcrypt.gensalt()).decode()

        # create the user and return the user object to the caller so he can save this ID in 
        #   the session variable
        return self.create(
            first_name = post_data['first_name'],
            last_name = post_data['last_name'],
            email = post_data['email'],
            password = hashed_pw 
        )

    # return true or false depending on if they authenticate correctly or not
    def authenticate(self, email, password):
        # check for the email existence in the system
        #   User.object == self here since this is part of the manager / objects property in the User class
        user_acct = self.filter(email=email)

        if len(user_acct) < 1:
            # the email address was not found in the User table
            return False
        
        # grab and return the first result as a single object and NOT a list
        user = user_acct[0]
        # comparing the password saved with the one passed in will return a boolean
        #   we have to encode the one passed in so that when it is hashed it will match what we saved to the DB
        return bcrypt.checkpw(password.encode(), user.password.encode())


class User(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

