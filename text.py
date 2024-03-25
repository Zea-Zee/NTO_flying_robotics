import cv2
from PIL import Image
import pytesseract


img = cv2.imread('./car.jpg')


def recognize_text(image):
    image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789АВЕКМНОРСТУХ'
    text = pytesseract.image_to_string(image_pil, config=custom_config)
    return text


print(recognize_text(img))
