from rest_framework import viewsets
from .models import CustomUser, Parcel, DeliveryProof
from .serializers import CustomUserSerializer, DeliveryProofSerializer, ForCourierSerializer, ForCustomerSerializerUpdate, ForAdminSerializer, ForCustomerSerializerWrite
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import ParcelPermissionObjLevel, ParcelPermissionModelLevel, ProofPermissionObjLevel, ProofPermissionModelLevel


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
   serializer_class = MyTokenObtainPairSerializer  


# Create your views here.
class ParcelViewSet(viewsets.ModelViewSet):
  permission_classes = [ParcelPermissionObjLevel, ParcelPermissionModelLevel]

  def get_queryset(self, *args, **kwargs):
    current_user = self.request.user
    if current_user:
      query =  Parcel.objects.filter(courier=current_user)
      if query: 
        return query
     
      else:
        return Parcel.objects.all()
      
      
  def get_serializer_class(self):
        if self.request.method == "POST" and self.request.user.customer:
           return ForCustomerSerializerWrite
        if self.request.user.customer:
            return ForCustomerSerializerUpdate
        if self.request.user.courier:
           return ForCourierSerializer
        else:
           return ForAdminSerializer   


class DeliveryProofViewSet(viewsets.ModelViewSet):
  serializer_class = DeliveryProofSerializer
  permission_classes = [ProofPermissionObjLevel, ProofPermissionModelLevel]

  def get_queryset(self, *args, **kwargs):
    current_user = self.request.user

    if current_user and current_user.courier:
       proofQuery = DeliveryProof.objects.filter(parcel__courier=current_user)
       return proofQuery
    if current_user and current_user.customer:
      proofQuery = DeliveryProof.objects.filter(parcel__sender=current_user)
      return proofQuery
    if current_user and current_user.admin:
      return DeliveryProof.objects.all()
       

    

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