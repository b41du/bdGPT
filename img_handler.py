from config import images_default_path, img_destination_path, font_path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
from slugify import slugify

class ImgHandler:

    def __init__(self):
        self.default_img_path = images_default_path[random.randint(0, len(images_default_path) -1)]
        self.destination_path = img_destination_path
        self.font = font_path

    def get_text(self, keyword=''):
        if len(keyword) > 20:
            return keyword[:20] + '...'
        return keyword
    
    def generate_filename(self, keyword):
        now_ = datetime.now()
        filename = slugify(keyword)[:10] + '_'
        filename = filename + now_.strftime('%Y%m%d_%H%M%S') + '.jpg'
        
        return filename
    
    def generate_images(self, keyword=''):
        img = Image.open(self.default_img_path)
        w, h = img.size
        draw = ImageDraw.Draw(img)
        font_ = ImageFont.truetype(self.font, 60, encoding="unic")
        draw.text(xy=(w/2, h/2), text=self.get_text(keyword), font=font_, anchor='mm', fill='black')
        save_path = img_destination_path + self.generate_filename(keyword)
        
        if img.save(save_path):
            return save_path
        
        return False

# if __name__ == "__main__":
#     imgh = ImgHandler()
#     imgh.generate_images(keyword='Node.js应用程序在崩溃新启动')