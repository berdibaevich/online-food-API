import os
import re


def get_upload_path(instance, filename):
    """
        Bunin' waziypasi saqlanip atirg'an obiektimiz image m-n
        isleydi.
        Misali:
            62shs6as.webp -> product_name.webp
    """
    filename, ext = os.path.splitext(filename)
    return os.path.join(instance.__class__.__name__.lower() + "_images", f"{instance.slug}{ext}")



def get_slugify(value):
    """
        self.name object di slugify qilip beredi
        Misali:
            - Russion kartoshka -> russion-kartoshka
            - Samsa 22 -> samsa-22
    """
    name = value.lower()
    slug_name = re.sub(r"\s", "-", name)
    return slug_name