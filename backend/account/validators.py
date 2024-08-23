import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_uzb_phone_number(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(
            _('%(value)s bul O\'zbekistan telefon no\'meri emes.'),
            params={'value': value},
        )