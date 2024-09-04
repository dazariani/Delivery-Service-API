from rest_framework import viewsets
from .models import CustomUser, Parcel, DeliveryProof
from .serializers import CustomUserSerializer, ParcelSerializer, DeliveryProofSerializer


# Create your views here.
class ParcelViewSet(viewsets.ModelViewSet):
  queryset = Parcel.objects.all()
  serializer_class = ParcelSerializer


class DeliveryProofViewSet(viewsets.ModelViewSet):
  queryset = DeliveryProof.objects.all()
  serilizer_class = DeliveryProofSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer