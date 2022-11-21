import os
import textwrap
from datetime import datetime
from typing import Union

from matplotlib import font_manager, colors
from PIL import Image, ImageDraw, ImageFont


class Watermarker:
    def __init__(
        self,
        image_path,
        font_file: str = '',
        text_color: Union[str, tuple] = '#fff',
    ):
        self._image_path = image_path
        self._font_file = font_file
        self._text_color = text_color

    @property
    def image(self):
        try:
            return Image.open(self._image_path)
        except FileNotFoundError:
            raise FileNotFoundError(f'Cannot open image {self._image_path}')

    @property
    def image_rgba(self):
        return self.image.convert('RGBA')

    @property
    def font_file(self):
        if self._font_file and not os.path.exists(self._font_file):
            font_file_name = os.path.basename(self._font_file)
            font_name = os.path.splitext(font_file_name)[0]
            font_props = font_manager.FontProperties(family=font_name)
            try:
                font = font_manager.findfont(
                    font_props, fallback_to_default=False
                )
                return font
            except ValueError:
                raise ValueError(f'Unable to find font {self._font_file}')

        elif self._font_file and os.path.exists(self._font_file):
            return self._font_file
        else:
            font = font_manager.FontProperties(
                family='sans-serif', weight='normal'
            )
            return font_manager.findfont(font)

    def _get_color(self, color, alpha) -> tuple:
        converted = colors.to_rgba(color, alpha=alpha)
        return tuple(round(x * 255) for x in converted)

    def _get_text_size(self, text, font_size):
        font = ImageFont.truetype(self.font_file, font_size)
        return font.getsize(text)

    def _get_font_size(self, text: str, mode: str = ''):
        font_size = 1
        fraction = 0.2

        if mode == 'watermark':
            fraction = 0.5
        elif mode == 'timestamp':
            fraction = 0.22

        image_width = self.image.size[0]
        while self._get_text_size(text, font_size)[0] < fraction * image_width:
            font_size += 1

        return font_size

    def _calc_position(self, text, font_size, ptype='', mode='') -> tuple:
        # To-do
        # Calculate based on image size and text size
        # Support keywords: tl, tc, tr, cc, bl, bc, br
        width, height = self.image.size
        text_with, text_height = self._get_text_size(text, font_size)
        return ((width - text_with) / 2, (height - text_height) / 2)

    def _get_image_timestamp(self, fmt: str):
        exif = self.image.getexif()
        creation_time = exif.get(306)
        if not creation_time:
            raise ValueError('Unable to get image timestamp')
        timestamp_dt = datetime.strptime(creation_time, '%Y:%m:%d %H:%M:%S')
        return datetime.strftime(timestamp_dt, fmt)

    def _get_filename(self, suffix):
        path, ext = os.path.splitext(self._image_path)
        return f'{path}_{suffix}{ext}'

    def _draw_text(self, suffix, position, text, font_size, text_color):
        image = self.image_rgba
        txt = Image.new('RGBA', self.image_rgba.size, (255, 255, 255, 0))
        d = ImageDraw.Draw(txt)
        font = ImageFont.truetype(self.font_file, font_size)
        d.text(
            position,
            text,
            fill=text_color,
            font=font,
        )
        result = Image.alpha_composite(image, txt)
        result.show()
        image_rgb = result.convert('RGB')
        image_rgb.save(self._get_filename(suffix))

    def add_timestamp(
        self,
        fmt: str = '%Y/%m/%d %H:%M',
        timestamp: str = '',
        font_size: int = 0,
        text_color: Union[str, tuple] = 'white',
        text_transparency: float = 1.0,
        position=(0, 0),
    ):
        color = self._get_color(text_color, text_transparency)
        if not timestamp:
            timestamp = self._get_image_timestamp(fmt)
        if not font_size:
            font_size = self._get_font_size(timestamp, mode='timestamp')

        self._draw_text('timestamped', position, timestamp, font_size, color)

    def add_watermark(
        self,
        text: str,
        font_size: int = 0,
        text_color: Union[str, tuple] = 'white',
        text_transparency: float = 0.3,
        position=(0, 0),
    ):
        color = self._get_color(text_color, text_transparency)
        if not font_size:
            font_size = self._get_font_size(text, mode='watermark')

        if position == (0, 0):
            position = self._calc_position(text, font_size, mode='watermark')

        self._draw_text('watermarked', position, text, font_size, color)
