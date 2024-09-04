from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
  admin = models.BooleanField(default=False)
  customer = models.BooleanField(default=False)
  courier = models.BooleanField(default=False)

  

class Parcel(models.Model):
  PARCEL_STATUS_CHOICES = [
  ("Pending", "Pending"),
  ("In Transit", "In Transit"),
  ("Delivered", "Delivered"),
  ]
  
  title = models.CharField(max_length=50)
  description = models.TextField(max_length=200)
  status = models.CharField(choices=PARCEL_STATUS_CHOICES)
  sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
  receiver_name = models.CharField(max_length=50)
  receiver_address = models.TextField(max_length=150)
  courier = models.ForeignKey(CustomUser, related_name='courier_parcels', null=True, blank=True, on_delete=models.CASCADE) 
  created_at = models.DateTimeField(auto_now_add=True)
  delivered_at = models.DateTimeField(null=True, blank=True)

  def __str__(self):
    return self.title


class DeliveryProof(models.Model):
  parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE) 
  image = models.ImageField(upload_to='images/')
  timestamp = models.DateTimeField(auto_now_add=True) 

  def __str__(self):
    return self.parcel.title + ' delivery proof'
