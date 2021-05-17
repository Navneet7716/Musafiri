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


class Flight(models.Model):
    companyName = models.CharField(max_length=30)
    sourceLocation = models.CharField(max_length=30)
    destinationLocation = models.CharField(max_length=30)
    departureDate = models.DateField()
    departureTime = models.TimeField()
    fareEconomy = models.DecimalField(max_digits=6,decimal_places=2)
    fareBusiness = models.DecimalField(max_digits=6,decimal_places=2)
    fareFirst = models.DecimalField(max_digits=6,decimal_places=2)
    numSeatsRemainingEconomy = models.IntegerField()
    numSeatsRemainingBusiness = models.IntegerField()
    numSeatsRemainingFirst = models.IntegerField()


    def __str__(self):
        return self.companyName


class Train(models.Model):
    companyName = models.CharField(max_length=30)
    sourceLocation = models.CharField(max_length=30)
    destinationLocation = models.CharField(max_length=30)
    departureDate = models.DateField()
    departureTime = models.TimeField()
    fareEconomy = models.DecimalField(max_digits=8,decimal_places=2)
    fareBusiness = models.DecimalField(max_digits=8,decimal_places=2)
    fareFirst = models.DecimalField(max_digits=10,decimal_places=2)
    numSeatsRemainingEconomy = models.IntegerField()
    numSeatsRemainingBusiness = models.IntegerField()
    numSeatsRemainingFirst = models.IntegerField()

    def __str__(self):
        return self.companyName


class Hotel(models.Model):
    hotelName = models.CharField(max_length=50,default='hotel')
    hotel_type = models.IntegerField()
    hotel_image = models.ImageField(upload_to='images/')
    dailyCost = models.DecimalField(max_digits=8,decimal_places=2)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    

    def __str__(self):
        return self.hotelName

    
