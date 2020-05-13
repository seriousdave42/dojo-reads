from django.db import models
import re
from datetime import datetime, timedelta

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        NAME_REGEX = re.compile(r'^[a-zA-Z\s]{2,}$')
        if not NAME_REGEX.match(post_data["name"]):
            errors["name"] = "Name must be at least two characters long, letters and spaces only"
        if len(post_data["user_name"]) < 6:
            errors["user_name"] = "User name must be at least six characters long"
        elif User.objects.filter(user_name = post_data["user_name"]):
            errors["user_name"] = "User name already exists"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address"
        elif len(User.objects.filter(email = post_data['email'])) > 0:
            errors['email'] = "Email already exists"
        PW_REGEX = re.compile(r'^(?=.*cat)(?=.*5)[a-zA-Z0-9]{8,}$')
        if not PW_REGEX.match(post_data['password']):
            errors['password'] = "Password must be at least 8 characters and contain \"cat\", the number 5, and no special characters"
        if not post_data['password'] == post_data['pw_check']:
            errors['pw_check'] = "Passwords do not match!"
        return errors
    
        
class User(models.Model):
    name = models.CharField(max_length = 255)
    user_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 80)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()