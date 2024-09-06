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
    

class ParcelPermissionModelLevel(permissions.BasePermission):

  def has_permission(self, request, view):
    if(request.method == 'POST' and request.user.customer == False and request.user.admin == False):
      return False
    if(view.action == 'list' and request.user.customer):
      return False
    return True
  

# Delivery proof permissions
class ProofPermissionObjLevel(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    # courier
    if request.user.courier and obj.parcel.courier.id == request.user.id and request.method in permissions.SAFE_METHODS:
      return True
    
    # customer
    if request.user.customer and obj.parcel.sender.id == request.user.id and request.method in permissions.SAFE_METHODS:
      return True
    
    # admin 
    if request.user.admin:
      return True
    

class ProofPermissionModelLevel(permissions.BasePermission):

  def has_permission(self, request, view):
    if(request.method == 'POST' and request.user.courier == False and request.user.admin == False):
      return False
    return True
  

# User permissions
class UserPermissionObjLevel(permissions.BasePermission):

  def has_object_permission(self, request, view, obj):

    if request.user.admin:
      return True
    

class UserPermissionModelLevel(permissions.BasePermission):

  def has_permission(self, request, view):

    if(request.user.is_anonymous == False and request.user.admin):
      return True
    




    



  