from django.core.exceptions import ValidationError


def validate_rating(value):
    """
        Validate rating before save into the table :)
    """
    valid_ratings = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    if value not in valid_ratings:
        raise ValidationError("Invalid rating value. Valid options are: 0.5, 1, 1.5, ..., 4.5, 5.")
