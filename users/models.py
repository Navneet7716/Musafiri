from django.db import models


# Create your models here.

class Destination(models.Model):
    destination_image = models.ImageField(upload_to='images/')
    destination_name = models.CharField(max_length=50)
    destination_description = models.CharField(max_length=200)
    package_price = models.IntegerField()
    

    def __str__(self):
        return self.destination_name

class blog_user(models.Model):
    blog_image = models.ImageField(upload_to = 'images/')
    blog_heading = models.CharField(max_length=100)
    blog_desc = models.CharField(max_length=200)
    blog_date = models.DateTimeField()


    def __str__(self):
        return self.blog_heading