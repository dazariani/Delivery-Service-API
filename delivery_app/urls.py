from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ParcelViewSet, DeliveryProofViewSet, MyTokenObtainPairView, UserView, Register

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'parcels', ParcelViewSet, basename='ParcelModel')
router.register(r'deliveryProofs', DeliveryProofViewSet, basename='ProofModel')

urlpatterns = [
    path('', include(router.urls)),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('me', UserView.as_view()),
    path('register', Register.as_view()),
]


