from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from .utils import get_slugify, get_upload_path
from .validators import (validate_discount_percent_maximum,
                         validate_discount_percent_of_positive,
                         validate_if_not_discount_percent, validate_max_digits,
                         validate_parent_category_image, validate_positive)

# from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.


# CATEGORY TABLE
class Category(models.Model):
    """
        Category Table 
    """ 
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("category name"),
        help_text=_("Format: required, max-100")
    )
    slug = models.SlugField(
        blank=True,
        max_length=100, unique=True,
        verbose_name=_("SAFE URL"),
        help_text=_("format: required, letter, numbers, underscore.")
    )
    image = ResizedImageField(
        verbose_name=_("The image for the category"),
        upload_to = get_upload_path,
        help_text = _("format: required"),
        #validators = [validate_parent_category_image]
    )
    is_active = models.BooleanField(
        _("Is active"),
        default=True,
        help_text=_("defaul: True, if False will not show to customers")
    )

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")


    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        slug_name = get_slugify(self.name)
        self.name = self.name.capitalize() # Always save upper first character of object ok :)
        self.slug = slug_name
        super().save(*args, **kwargs)
# END CATEGORY TABLE 


# PRODUCT TABLE
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_("product name"),
        help_text=_("format: required, max-200")
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name=_("Product SAFE URL"),
        help_text=_("format: required, letters, numbers etc"),
        blank=True
    )
    description = models.TextField(
        verbose_name=_("product description"),
        help_text=_("format: required")
    )
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        unique=False,
        verbose_name=_("original price"),
        help_text=_("format: maximum price 99999999.99"),
        error_messages={
            "name":{
                "max_lenght": _("the price must be between 0 and 99999999.99")
            }
        },
        validators=[validate_positive, validate_max_digits]
    )
    discount_percent = models.DecimalField(
        _("discount percentage"),
        max_digits=4,
        decimal_places=2,
        help_text=_("format: not required"),
        null=True,
        blank=True,
        validators=[validate_discount_percent_of_positive, validate_discount_percent_maximum]
    )
    discounted_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        unique=False,
        null=True,
        blank=True,
        verbose_name=_("discounted price"),
        help_text=_("format: the maximum price is 99999999.99, but it will be a discounted price, so it will be less than the original price, and also when the discount percentage is met, it will be automatically saved :)"),
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("product quantity"),
        default=1
    )
    image = ResizedImageField(
        _("product image"),
        upload_to = get_upload_path,
        help_text=_("format: not required"),
        blank = True,
        null = True,
        default = "product_images/no-food.webp"
    )
    ingredients = models.ManyToManyField(
        "Ingredient",
        verbose_name=_("product ingredients"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("product visibility"),
        help_text=_("format: true=product visible")
    )
    created_at = models.DateTimeField(
        auto_now_add= True,
        verbose_name=_("date product created"),
        help_text=_("format: Y-m-d H:M:S")
    )
    updated_at = models.DateTimeField(
        auto_now= True,
        verbose_name=_("date product last updated"),
        help_text=_("format: Y-m-d H:M:S")
    )


    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug_name = get_slugify(self.name)
        self.slug = slug_name
        # 
        if self.original_price and self.discount_percent:
            discount_amount = self.original_price * (self.discount_percent / 100)
            self.discounted_price = self.original_price - discount_amount
        super().save(*args, **kwargs)


    def clean(self) -> None:
        super().clean()
        validate_if_not_discount_percent(self.discounted_price, self.discount_percent)
# END PRODUCT TABLE 


# FOR INGREDIENT TABLE
class Ingredient(models.Model):
    name = models.CharField(_("ingredient name"), max_length=150, unique=False)

    def __str__(self):
        return f"{self.name}, id {self.pk}"

# class Ingredient(models.Model):
#     UNIT = (
#         ('Gram', 'Gram'),
#         ('Milligram', 'Milligram'),
#         ('Kilogram', 'Kilogram'),
#         ('Liter', 'Liter'),
#         ('U\'lken qasiq', 'U\'lken qasiq'), # TABLESPOON
#         ('Kishkene qasiq', 'Kishkene qasiq'), # TEASPOON
#         ('Meter', 'Meter'),
#         ('Centimeter', 'Centimeter'),
#         ('Shtuk', 'Shtuk'),
#         ('Stakan', 'Stakan'), #Cup
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ingredients")
#     name = models.CharField(_("ingredient name"), max_length=100)
#     quantity = models.FloatField(
#         _("weight/quantity"),
#         unique=False
#     )
#     unit = models.CharField(
#         _("O'lshemileri"),
#         max_length=25,
#         choices=UNIT
#     )

#     class Meta:
#         constraints = [
#             UniqueConstraint(fields=['product', 'name'], name='unique_product_ingredient')
#         ]
    
#     def save(self, *args, **kwargs):
#         self.name = self.name.capitalize
#         return super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name}, id {self.pk}"
# END FOR INGREDIENT TABLE 