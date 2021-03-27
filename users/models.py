from django.db import models


# Create your models here.

class Destination(models.Model):
    destination_image = models.ImageField(upload_to='images/')
    destination_name = models.CharField(max_length=50)
    destination_description = models.CharField(max_length=200)
    package_price = models.IntegerField()
    

    def __str__(self):
        return self.destination_name
