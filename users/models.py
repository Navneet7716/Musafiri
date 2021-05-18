from django.db import models


# Create your models here.

class Destination(models.Model):
    destination_image = models.ImageField(upload_to='images/')
    destination_name = models.CharField(max_length=50)
    destination_description = models.CharField(max_length=200)
    package_price = models.IntegerField()
    banner_image = models.ImageField(upload_to='images/', null=True)

    

    def __str__(self):
        return self.destination_name

class blog_user(models.Model):
    blog_image = models.ImageField(upload_to = 'images/', null=True)
    blog_heading = models.CharField(max_length=100)
    blog_desc = models.CharField(max_length=200)
    blog_date = models.DateField()
    createdBy = models.CharField(max_length=250, null=True)

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
    companyName = models.CharField(max_length=300)
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

    
class History_Flight(models.Model):
    user = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    obj_date = models.DateField()
    obj_time = models.TimeField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)

    def __str__(self):
        return self.user

class History_Train(models.Model):
    user = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    obj_date = models.DateField()
    obj_time = models.TimeField()
    price = models.DecimalField(max_digits=8 , decimal_places=2)

    def __str__(self):
        return self.user

class History_Package(models.Model):
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.user


class History_Hotel(models.Model):
    user = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    type = models.IntegerField()
    image = models.ImageField(upload_to="images/")
    price = models.DecimalField(max_digits=8,decimal_places=2)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


    def __str__(self):
        return self.user