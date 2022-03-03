import os
import random

import pytest

from converter import convert_image
from utils import FORMATS, get_input_format, get_filename


input_files = [
    os.path.join('files/input', file) for file in os.listdir('files/input')
]

urls = [
    'https://cdn.pixabay.com/photo/2016/05/02/13/17/deer-1367217_1280.jpg',
    'https://images.unsplash.com/photo-1643188438863-3a65f0f3c26f?fit=crop&w=1023&q=80',
    'https://images.pexels.com/photos/2265247/pexels-photo-2265247.jpeg?auto=compress&h=750&w=1260',
]

output_dir = 'files'


def test_covert_image():
    images = input_files + urls

    for image in images:
        image_format = get_input_format(image)
        different_formats = [i for i in FORMATS if i != image_format.lower()]
        random_format = random.choice(different_formats)

        assert convert_image(image, random_format, output_dir)
        new_file = f'{get_filename(image)}.{random_format}'
        assert os.path.exists(os.path.join(output_dir, new_file))


# def test_covert_image_with_invalid_values():
#     with pytest.raises(Exception):
#         pass
