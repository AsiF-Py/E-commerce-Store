from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager




class Account(AbstractUser):
    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=255,unique=True)  # changes email to unique and blank to false
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS



class Address(models.Model):
    user = models.ForeignKey(Account,blank=True,null=True,on_delete=models.CASCADE,related_name='user_address')
    company_name = models.CharField(max_length=255,blank=True, null=True)
    street_address = models.CharField(max_length=255,blank=True, null=True)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=15,blank=True, null=True)  # You might want to adjust the max_length based on your requirements
    email_address = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} - {self.town_city}"