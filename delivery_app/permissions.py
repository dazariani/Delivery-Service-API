from rest_framework import permissions
from .models import Parcel, DeliveryProof


# Parcel permissions
class ParcelPermissionObjLevel(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    # customer
    if request.user.customer and obj.sender.id == request.user.id:
      return True
    
    # courier
    if request.user.courier and obj.courier.id == request.user.id:
      return True
    
    # admin 
    if request.user.admin:
      return True
    

# class ParcelPermissionModelLevel(permissions.BasePermission):



  