from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser) :
    apmnt_name = models.CharField(max_length=30)
    phone = models.IntegerField()


