import hashlib
import os

from django.utils.text import get_valid_filename


def generate_unique_filename(instance, filename):
    """
        This is generated unique image's name for us 
    """
    user_id = instance.id
    # Get the original filename and sanitize it
    original_filename = get_valid_filename(os.path.basename(filename))
    # Generate a short hash based on the original filename
    short_hash = hashlib.md5(original_filename.encode()).hexdigest()[:6]
    # Combine the parts to form the unique filename
    unique_filename = f"user_{user_id}_{short_hash}_{original_filename}"
    # Return the full path for the image
    return os.path.join('avatars', unique_filename)