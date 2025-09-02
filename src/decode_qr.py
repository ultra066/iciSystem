import sys
import os
sys.path.append('.')

from pyzbar.pyzbar import decode
from PIL import Image

qr_path = 'qr_codes/60dcc885_qr.png'
if os.path.exists(qr_path):
    image = Image.open(qr_path)
    decoded_objects = decode(image)
    if decoded_objects:
        qr_code = decoded_objects[0].data.decode("utf-8")
        print(f"Decoded QR code: {qr_code}")
    else:
        print("No QR code found in the image.")
else:
    print(f"QR code image not found at {qr_path}")
