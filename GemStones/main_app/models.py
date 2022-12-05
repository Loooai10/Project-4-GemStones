from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
# ./home/models.py
class Product(models.Model):
   name = models.CharField(max_length=150)
   price = models.DecimalField(max_digits=6, decimal_places=2)
   description = models.TextField()
   image = models.CharField(max_length=5000, null=True, blank=True)
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   
def __str__(self):
    return self.name   