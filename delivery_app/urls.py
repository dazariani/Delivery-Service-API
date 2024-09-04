from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ParcelViewSet, DeliveryProofViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'Parcels', ParcelViewSet)
router.register(r'DeliveryProofs', DeliveryProofViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


