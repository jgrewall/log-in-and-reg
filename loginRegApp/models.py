from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors ={}
        if len(postData['fName'])<2:
            errors['errorfName']= 'First name needs to be longer then 2 characters'
        if len(postData['lName'])<2:
            errors['errorlName']= 'Last name need to be longer then 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['erroremail']='Invalid email address'
        if len(User.objects.filter(email=postData['email']))>0:
            errors['erroremailexists']='This address is already taken'
        if len(postData['password'])<8:
            errors['errorpassword']= 'Password need to be longer then 8 characters'
        if postData['password'] != postData['confirmPW']:
            errors['errorconfirmPW']='Your passwords dont seem to match'
        return errors
    def login_validator(self, postData):
        errors={}
        if not EMAIL_REGEX.match(postData['email']):
            errors['formatemail'] = 'Not a valid email format'
        if not User.objects.filter(email=postData['email']):
            errors['Wrongemail']='wrong password'
        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)