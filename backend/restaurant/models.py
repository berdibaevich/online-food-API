import os

from backend.account.validators import validate_uzb_phone_number
from backend.product.utils import get_slugify
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from .utils import generate_qr_code
from .validators import validate_rating

# Create your models here.

# Restaurant TABLE
class Restaurant(models.Model):
    name = models.CharField(
        _("restaurant name"), 
        max_length=150, unique=True, 
        help_text=_("format: required, max-150")
        )
    slug = models.SlugField(
        blank=True,
        max_length=100, unique=True,
        verbose_name=_("SAFE URL"),
        help_text=_("format: required, letter, numbers, underscore.")
    )
    about_us = models.TextField(
        _("about us"),
        help_text=_("format: required")
    )
    phone_number1 = models.CharField(
        _("first phone number"),
        help_text=_("format: required"),
        unique=True,
        max_length=13,
        validators=[validate_uzb_phone_number]
    )
    phone_number2 = models.CharField(
        _("second phone number"),
        help_text=_("format: not required"),
        unique=True,
        null=True, blank=True,
        max_length=13,
        validators=[validate_uzb_phone_number]
    )
    telegram_link = models.CharField(
        _("social telegram"),
        max_length=100,
        help_text=_("format: not required, max-100"),
        null=True, blank=True
    )
    instagram_link = models.CharField(
        _("social instagram"),
        max_length=100,
        help_text=_("format: not required, max-100"),
        null=True, blank=True
    )
    facebook_link = models.CharField(
        _("social facebook"),
        max_length=100,
        help_text=_("format: not required, max-100"),
        null=True, blank=True
    )
    domain_name = models.CharField(
        _("domain name"),
        max_length=255,
        help_text=_("format: required, max-255"),
    )
    qr_code = models.ImageField(
        _("qr code"),
        upload_to=('qr_codes'),
        blank=True,
        null=True,
        help_text=_("format: required, itself generated qr code for you.")
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name=_("date restaurant created"),
        help_text=_("format: Y-m-d H:M:S")
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        verbose_name=_("date restaurant last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )

        
    class Meta:
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurant")


    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        self.slug = get_slugify(self.name)
        sanitized_name = slugify(self.domain_name)
        fname = f'qr_code-{sanitized_name}.png'
        logo_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes/logo.jpg')
        qr_code_img = generate_qr_code(self.domain_name, logo_path=logo_path)

        qr_code_file = os.path.join(settings.MEDIA_ROOT, 'qr_codes', fname)
        qr_code_img.save(qr_code_file, 'PNG')
        self.qr_code = os.path.join('qr_codes', fname)
        super().save(*args, **kwargs)
# END Restaurant TABLE


# ADDRESS TABLE
class Address(models.Model):
    town_city = models.CharField(
        _("Town/City/State"),
        max_length=150,
        help_text=_("format: required, max-150")
    )
    address_line = models.CharField(
        _("address line 1"),
        max_length=255,
        help_text=_("format: required, max-255")
    )
    address_line2 = models.CharField(
        _("address line 2"),
        max_length=255,
        help_text=_("format: not required, max-255"),
        blank=True,
        null=True
    )
    is_default = models.BooleanField(
        _("company default address"),
        default=False,
        help_text=_("format: not required, only one address is_default=True")
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name=_("date address created"),
        help_text=_("format: Y-m-d H:M:S")
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        verbose_name=_("date address last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    
    def __str__(self):
        return self.town_city
# END ADDRESS TABLE 


# MEDIA TABLE
class Media(models.Model):
    """
        The Restaurant image table 
    """
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name=("restaurant_images"),
    )
    image = ResizedImageField(
        _("restaurant image"),
        upload_to = "restaurant_images/",
        blank = True,
        null = True
    )
    alt_text = models.CharField(
        _("alternative text"),
        max_length=150,
        help_text=_("format: required, max-150. So this is about of restaurant image")
    )
    is_feature = models.BooleanField(
        _("product default image"),
        default=False,
        help_text=_("format: default=False, true=default image")
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        editable=False,
        verbose_name=_("date restaurant image created"),
        help_text=_("format: Y-m-d H:M:S")
    )

    updated_at = models.DateTimeField(
        auto_now= True,
        editable=False,
        verbose_name=_("date restaurant image last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )

    class Meta:
        verbose_name = _("restaurant image")
        verbose_name_plural = _("restaurant images")


    def __str__(self):
        return self.alt_text
# END MEDIA TABLE 


# REVIEW RATING TABLE
class Feedback(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="restaurant_feedback"
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_feedback"
    )
    rating = models.FloatField(
        _("rating"),
        help_text=_("format: required, 0.5, 1.0 ..... 4.5, 5.0"),
        validators=[validate_rating]
    )
    feedback = models.TextField(
        _("feedback of user"),
        max_length=1000,
        help_text=_("format: required, max-1000")
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        editable=False,
        verbose_name=_("date feedback created"),
        help_text=_("format: Y-m-d H:M:S")
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        editable=False,
        verbose_name=_("date feedback last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )


    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Restaurant feedbacks")

    
    def __str__(self):
        return str(self.rating)
# END REVIEW RATING TABLE