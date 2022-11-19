import os
import re
from datetime import datetime

from matplotlib import font_manager
from PIL import Image, ImageDraw, ImageFont


class Watermarker:
    def __init__(self, image_path, font_file=None, text_color='#fff'):
        self.image_path: str = image_path
        self.position = ''
        self._font_file = font_file
        self._text_color = text_color

    @property
    def image(self):
        return Image.open(self.image_path)

    @property
    def font(self):
        if self._font_file and not os.path.exists(self._font_file):
            raise FileNotFoundError(
                f'Full path to font required. {self._font_file} does not exist'
            )
        elif self._font_file and os.path.exists(self._font_file):
            font_file = self._font_file
        else:
            font = font_manager.FontProperties(
                family='sans-serif', weight='normal'
            )
            font_file = font_manager.findfont(font)
        return ImageFont.truetype(font_file, 100)

    @property
    def text_color(self):
        match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', self._text_color)
        if not match:
            raise ValueError(
                f'{self._text_color} is not a valid hex value for text_color'
            )
        return self._text_color

    def get_image_timestamp(self, fmt: str):
        exif = self.image.getexif()
        creation_time = exif.get(306)
        if not creation_time:
            raise ValueError('Unable to get image timestamp.')
        timestamp_dt = datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
        return datetime.strftime(timestamp_dt, fmt)

    def add_timestamp(self, fmt: str = '%Y/%m/%d %H:%M'):
        image = self.image
        d = ImageDraw.Draw(image)
        width, height = image.size
        timestamp = self.get_image_timestamp(fmt=fmt)
        d.text(
            (width / 1.4, height / 1.1),
            timestamp,
            self.text_color,
            font=self.font,
        )
        image.show()

    def add_watermark(self, text):
        image = self.image.convert('RGBA')
        width, height = image.size
        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        d.text(
            (width / 2, height / 2),
            text,
            font=self.font,
            fill=(255, 255, 255, 128),
        )
        out = Image.alpha_composite(image, txt)
        out.show()
