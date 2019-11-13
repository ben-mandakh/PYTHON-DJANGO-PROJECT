from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self,postData):
        print("Inside Acountmanager Class Beginning")
        errors={}
        if len(postData['first_name'])<2:
            errors["first_name"]="First name should be at least two characters"
        if len(postData['last_name'])<2:
            errors["last_name"]="Last name should be at least two characters"
        if len(postData['password'])<8:
            errors["password"]="Password should be at least five characters"
        if postData['password']!= postData['confirm_password']:
            errors["confirm_password"]="Passwords should match!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"]="Email should be valid!"
        this_email=User.objects.filter(email=postData['email'])
        if len(this_email)>0:
            errors["email"]="User already exist!"
        print("Inside Acountmanager Class ending")
        return errors

class ItemManager(models.Manager):
    def item_validator(self,postData):
        errors={}
        if len(postData['title'])<3:
            errors["title"]="Item title must consist of at least 3 characters!"
        if len(postData['description'])<1:
            errors["description"]="Description of item required"
        if len(postData['price'])<1:
            errors["price"]="Description of item required"
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.TextField(max_length=128)
    password=models.TextField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    uploaded_by = models.ForeignKey(User, related_name="items",on_delete=models.CASCADE)          # ONE TO MANY RELATIONS HERE
    accounts_who_like = models.ManyToManyField(User, related_name="liked_items")     # MANY TO MANY RELATIONS HERE
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()