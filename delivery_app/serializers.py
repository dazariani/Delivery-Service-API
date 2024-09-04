from rest_framework import serializers
from .models import CustomUser, Parcel, DeliveryProof

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'username', 'password', 'admin', 'customer', 'courier']
    extra_kwargs = {
      'password': {'write_only': True}
    }

  def create(self, validated_data):
    password = validated_data.pop('password', None)
    instance = self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance
  

class ParcelSerializer(serializers.ModelSerializer):
  class Meta:
    model = Parcel
    fields = '__all__'  
    read_only_fields = ('title', 'description', 'sender', 'receiver_name', 'courier', 'receiver_address', 'created_at')


class DeliveryProofSerializer(serializers.ModelField):
  class Meta:
    model = DeliveryProof
    fields = '__all__'