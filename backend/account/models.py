from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from .utils import generate_unique_filename
from .validators import validate_uzb_phone_number

# Create your models here.

class CustomUserBaseManager(BaseUserManager):
    def create_superuser(self, phone_number, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('status', 'ADMINISTRATOR')


        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )

        return self.create_user(phone_number, password, **other_fields)


    
    def create_user(self, phone_number, password, **other_fields):
        if not phone_number:
            raise ValueError(_('You must provide a phone number.'))
        
        user = self.model(phone_number = phone_number, **other_fields)

        user.set_password(password)
        user.save()
        return user



class UserBase(AbstractBaseUser, PermissionsMixin):
    """
        UserBase table for customers & admins
    """
    STATUS_OF_USER = (
        ('CUSTOMER', 'Customer'),
        ('ADMINISTRATOR', 'Administrator'),
    )

    first_name = models.CharField(_("first_name"), max_length=255)
    last_name = models.CharField(_("last_name"), max_length=255, null=True, blank=True)
    phone_number = models.CharField(_("phone_number"), max_length=13, unique=True, validators=[validate_uzb_phone_number])
    phone_token = models.CharField(max_length=6, null=True, blank=True)
    status = models.CharField(_("status"), max_length=15, choices=STATUS_OF_USER, default='CUSTOMER')
    avatar = ResizedImageField(
        _("avatar"),
        upload_to = generate_unique_filename,
        default = 'avatars/no_photo.png'
    )

    #User status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add= True,
        editable=False,
        verbose_name=_("date user created"),
        help_text=_("format: Y-m-d H:M:S")
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        editable=False,
        verbose_name=_("date user last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )
    expires_at = models.DateTimeField(
        _("expiry time of token"),
        null=True, 
        blank=True
    )

    objects = CustomUserBaseManager()
    
    USERNAME_FIELD = 'phone_number'


    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'
    

    def __str__(self):
        return f"{self.phone_number} & id is {self.pk}"
        
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" 




# class PhoneToken(models.Model):
#     phone_number = models.CharField(max_length=20, validators=[validate_uzb_phone_number])
#     token = models.CharField(max_length=6, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add= True)
#     expires_at = models.DateTimeField(null=True, blank=True)
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.token

#     class Meta:
#         verbose_name = "Sms token"
#         verbose_name_plural = "Sms Tokens"

