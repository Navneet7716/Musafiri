from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class extendedUser(models.Model):
    phoneno =  models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

