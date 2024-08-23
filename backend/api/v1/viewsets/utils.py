from django.core.files.storage import default_storage


def remove_image(image):
    """
        This is removed old image from media
        and if object will be deleted which is has image
        so remove from media
    """
    if default_storage.exists(image.path):
        default_storage.delete(image.path)