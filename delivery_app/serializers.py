from rest_framework import serializers
from .models import CustomUser, Parcel, DeliveryProof
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# My tokenObtain serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
# CustomUser serializer
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
  


# Parcel serializers
class ForCustomerSerializerUpdate(serializers.ModelSerializer):

  class Meta:
    model = Parcel
    fields = '__all__'
    read_only_fields = ('title', 'description', 'sender', 'receiver_name', 'status', 'courier', 'receiver_address', 'created_at')



class ForCustomerSerializerWrite(serializers.ModelSerializer):
  sender = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), queryset=CustomUser.objects.all())

  class Meta:
    model = Parcel
    fields = '__all__'
    


class ForCourierSerializer(serializers.ModelSerializer):
  class Meta:
    model = Parcel
    fields = '__all__'
    read_only_fields = ('title', 'description', 'sender', 'receiver_name', 'delivered_at', 'courier', 'receiver_address', 'created_at')


class ForAdminSerializer(serializers.ModelSerializer):
  class Meta:
    model = Parcel
    fields = '__all__'


# Delivery proof serializers
class DeliveryProofSerializer(serializers.ModelSerializer):
  class Meta:
    model = DeliveryProof
    fields = '__all__'