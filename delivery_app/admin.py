from django.contrib import admin
from .models import CustomUser, Parcel, DeliveryProof
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
  model = CustomUser
  add_form = CustomUserCreationForm


  fieldsets = (
    *UserAdmin.fieldsets,
    (
      'User role',
      {
        'fields': (
          'admin',
          'customer',
          'courier',
        )
      }
    ),
  )

  add_fieldsets = (
          (None, {'fields': ('username', 'password1', 'password2',
                              'admin', 'customer', 'courier',)}),
      )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Parcel)
admin.site.register(DeliveryProof)
