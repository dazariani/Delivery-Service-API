from rest_framework import viewsets, status
from .models import CustomUser, Parcel, DeliveryProof
from .serializers import CustomUserSerializer, DeliveryProofSerializer, ForCourierSerializer, ForCustomerSerializerUpdate, ForAdminSerializer, ForCustomerSerializerWrite, MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from .permissions import ParcelPermissionObjLevel, ParcelPermissionModelLevel, ProofPermissionObjLevel, ProofPermissionModelLevel, UserPermissionObjLevel, UserPermissionModelLevel
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, MultiPartParser


from rest_framework_simplejwt.views import TokenObtainPairView


# MyTokenObtainPairView
class MyTokenObtainPairView(TokenObtainPairView):
   serializer_class = MyTokenObtainPairSerializer  


# Parcel viewSet
class ParcelViewSet(viewsets.ModelViewSet):
  permission_classes = [ParcelPermissionObjLevel, ParcelPermissionModelLevel]

  # Filtering result
  filter_backends = [OrderingFilter, DjangoFilterBackend]
  ordering_fields = ['title', 'created_at']
  filterset_fields = ['title', 'status']
  
  
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
        elif self.request.user.customer:
            return ForCustomerSerializerUpdate
        elif self.request.user.courier:
           return ForCourierSerializer
        else:
          return ForAdminSerializer   


# Deliveryproof viewSet
class DeliveryProofViewSet(viewsets.ModelViewSet):
  serializer_class = DeliveryProofSerializer
  permission_classes = [ProofPermissionObjLevel, ProofPermissionModelLevel]
  parser_classes = [FormParser, MultiPartParser]


  # Filtering result
  filter_backends = [OrderingFilter, DjangoFilterBackend]
  ordering_fields = ['timestamp'] 
  filterset_fields = ['parcel__title',] 


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
       

# CustomUser viewSet
class UserViewSet(viewsets.ModelViewSet):
  queryset = CustomUser.objects.all()
  serializer_class = CustomUserSerializer
  permission_classes = (UserPermissionObjLevel, UserPermissionModelLevel)


   # Filtering result
  filter_backends = [OrderingFilter, DjangoFilterBackend]
  ordering_fields = ['username'] 
  filterset_fields = ['admin', 'customer', 'courier', 'username'] 



# Register
class Register(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)  
  

# Current user
class UserView(APIView):
    def get(self, request): 
        if not request.user.id:
            raise AuthenticationFailed('Unauthenticated :(')
        
        user = CustomUser.objects.filter(id=request.user.id).first()

        serializer = CustomUserSerializer(user)

        return Response(serializer.data)