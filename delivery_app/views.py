from rest_framework import viewsets
from .models import CustomUser, Parcel, DeliveryProof
from .serializers import CustomUserSerializer, ParcelSerializer, DeliveryProofSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
   serializer_class = MyTokenObtainPairSerializer  


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


# Current user
class UserView(APIView):
    def get(self, request): 
        if not request.user.id:
            raise AuthenticationFailed('Unauthenticated :(')
        
        user = CustomUser.objects.filter(id=request.user.id).first()

        serializer = CustomUserSerializer(user)

        return Response(serializer.data)