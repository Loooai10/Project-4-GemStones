from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
# ./home/models.py
# Create your models here.

     
class Buyer(models.Model):
    name = models.CharField(max_length=200,null=True)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



class Offer(models.Model):
       #  product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    buyer = models.ForeignKey(Buyer,null=True, on_delete=models.SET_NULL)
   #  product = models.ForeignKey(Product,null=True, on_delete=models.SET_NULL)
    date_offered = models.DateTimeField(auto_now_add=True)
    price_offered = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20,default= 'PENDING')
   #  def __str__(self):
   #      return self.buyer
     
    def get_absolute_url(self):
          return reverse('offers_detail', kwargs={'pk': self.id})
class Product(models.Model):
   name = models.CharField(max_length=150)
   price = models.DecimalField(max_digits=6, decimal_places=2)
   description = models.TextField()
   offers = models.ManyToManyField(Offer)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   def __str__(self):
      return self.name 
   
   def get_absolute_url(self):
      return reverse('detail', kwargs={'product_id': self.id}) 
   
   # change the default sort
   #  class Meta:
   #     ordering = ['-date_offered']
   
   
class UploadImage(models.Model):  
    caption = models.CharField(max_length=200)  
    image = models.ImageField(upload_to='images')  
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    def __str__(self):  
        return self.caption  