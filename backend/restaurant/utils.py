import qrcode
from PIL import Image


def generate_qr_code(url, logo_path, qr_color=(3, 58, 78)):
    """
    Generate QR code with a logo.
    """
    logo = Image.open(logo_path)
    basewidth = 100
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)

    qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr_code.add_data(url)
    qr_code.make()

    qr_image = qr_code.make_image(fill_color=qr_color, back_color="white").convert('RGB')

    pos = ((qr_image.size[0] - logo.size[0]) // 2, (qr_image.size[1] - logo.size[1]) // 2)
    qr_image.paste(logo, pos)

    return qr_image

# def generate_qr_code(url, logo_path, qr_color=(3, 58, 78)):
#     """
#         Generated qr code ok :)
#     """
#     logo = Image.open(logo_path)
#     basewidth = 100
#     wpercent = (basewidth / float(logo.size[0]))
#     hsize = int((float(logo.size[1]) * float(wpercent)))
#     logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

#     qr_code = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
#     qr_code.add_data(url)
#     qr_code.make()
    
#     qr_image = qr_code.make_image(fill_color=qr_color, back_color="white").convert('RGB')
    
#     pos = ((qr_image.size[0] - logo.size[0]) // 2, (qr_image.size[1] - logo.size[1]) // 2)
#     qr_image.paste(logo, pos)

#     return qr_image

