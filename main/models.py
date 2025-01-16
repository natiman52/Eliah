from django.db import models
from user.models import MyUser
from django.utils import timezone
# Create your models here.

class Images(models.Model):
    image =models.ImageField(upload_to="clothes/images/")
    def __str__(self):
        return self.image.name
class Product(models.Model):
    name = models.CharField(max_length=100)
    type =models.CharField(max_length=100,choices= [('F','Female'),('M',"Male"),('K',"Kids")],blank=True)
    images= models.ManyToManyField(Images)
    description =models.TextField()
    is_accessory=models.BooleanField(default=False)
    date = models.DateField(default=timezone.datetime.today,)
class Cart(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

class Subscribers(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.email