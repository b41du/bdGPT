from config import images_default_path, img_path_web_relative, images_custom_path, img_destination_path, font_path
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import random
import os
import glob
import logging

logging.basicConfig(level=logging.DEBUG)
class ImgHandler:

    def __init__(self):
        self.default_img_path = self.get_images_backgroud_path()
        self.font = font_path

    def get_images_backgroud_path(self):
        if os.path.exists(images_custom_path) and glob.glob("{}/*.jpg".format(images_custom_path)):
            images_paths = [os.path.join(images_custom_path, os.path.basename(x)) for x in glob.glob(images_custom_path + '*.jpg')]
        else:
            images_paths = [os.path.join(images_default_path, os.path.basename(x)) for x in glob.glob(images_default_path + '*.jpg')]

        return images_paths[random.randint(0, len(images_paths) -1)]

    def get_text(self, keyword=''):
        if len(keyword) > 20:
            return keyword[:20] + '...'
        return keyword

    def generate_filename(self, keyword):
        now_ = datetime.now()
        filename = '{}-{}{}'.format(str(hash(keyword)), now_.strftime('%Y%m%d_%H%M%S'), '.jpg')
        return filename

    def get_full_path(self, dynamic_path):
        static_path = img_destination_path
        folder_path = os.path.join(static_path, dynamic_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        return folder_path

    def generate_images(self, keyword=''):
        try:
            img = Image.open(self.default_img_path)
            w, h = img.size
            draw = ImageDraw.Draw(img)
            font_ = ImageFont.truetype(self.font, 60, encoding="unic")
            draw.text(xy=(w/2, h/2), text=self.get_text(keyword), font=font_, anchor='mm', fill='black')
            dynamic_path = img_path_web_relative.format(datetime.now().strftime('%Y/%m/%d/'))
            filename = self.generate_filename(keyword)
            save_path = self.get_full_path(dynamic_path) + filename
            img.save(save_path)
            
            if glob.glob(save_path):
                return '/{}{}'.format(dynamic_path, filename)

        except Exception as e:
            logging.error(str(e))
            return False

# if __name__ == "__main__":
#     imgh = ImgHandler()
#     imgh.generate_images(keyword='Node.js应用程序在崩溃新启动')