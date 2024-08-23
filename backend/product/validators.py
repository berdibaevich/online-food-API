from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_parent_category_image(value):
    """
        ONIN' WAZIYPASI CATEGORY MODELDEGI IMAGE FIELD
        USHIN TEK G'ANA PARENT KE QOSA ALADI IMAGE DI
        YAG'NIY WAZIYPASI QADAG'ALAP TURIW EGER SOL PARENTTIN' CHILDREN
        GE IMAGE QOSATIN BOLSA ERROR BEREDI.
    """
    if value and value.instance.parent:
        raise ValidationError(_("Child categories cannot have an image."))


# FOR ORIGINAL_PRICE
def validate_positive(value):
    """
        BUNIN' WAZIYPASI ORIGINAL PRICE FIELD DI QADAG'ALAW
        YAG'NIY TEK G'ANA POSITIVE SANNAN IBARAT BOLG'AN PRICE
        KIRITIW USHIN FUNCTION :)
    """
    if value <= 0:
        raise ValidationError(_("The price must be positive."))



def validate_max_digits(value):
    """
        BELGILENGEN MAX DIGIT OTIP KETPEWIN TAMINLEYDI OK :) 
    """
    max_digits = 10
    if len(str(value)) > max_digits:
        raise ValidationError(_("The price cannot exceed 10 digits."))
# END FOR ORIGINAL_PRICE


# FOR discounted_price
def validate_if_not_discount_percent(value, discount_percent = None):
    message = """
            -- Shegirmeli procent di kirgizbey saqlay almaysiz. 
            Jane bul jerge kirgiziwin'iz sha'rt emes o'zi avtomat
            tu'rde saqlaydi qashan siz discount percent di berip ketkennen
            keyin.
    """
    if value and discount_percent is None:
        raise ValidationError(message)
# END FOR discounted_price


# FOR # FOR discounted_percent FIELD
def validate_discount_percent_of_positive(value):
    if value <= 0:
        raise ValidationError(_("discount price tek g'ana positive boliwi kerek."))



def validate_discount_percent_maximum(value):
    _max = 99.99
    if _max < float(value):
        raise ValidationError("Maximum 99.99 saqlay alasiz.")
# END FOR discounted_percent FIELD
