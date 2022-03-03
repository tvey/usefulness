import argparse
import os

from PIL import Image

from utils import (
    is_url,
    get_filename,
    request_image,
    verify_output_format,
    verify_path,
)


def convert_image(value: str, out_format: str, save_to: str = '.'):
    if is_url(value):
        image = Image.open(request_image(value)).convert('RGB')
    else:
        image = Image.open(value).convert('RGB')

    if verify_output_format(out_format) and verify_path(save_to):
        verified_format = verify_output_format(out_format)
        filename = f'{get_filename(value)}.{verified_format}'
        pil_format = verified_format
        if verified_format == 'jpg':
            pil_format = 'jpeg'
        image.save(os.path.join(save_to, filename), pil_format)
        print('Image ready!')
        return True
    else:
        raise Exception('Unable to convert the image. Please check your input.')


parser = argparse.ArgumentParser(
    prog='Image Converter',
    usage='%(prog)s [options] image_path output_format save_to',
    description='Convert image to a desired format',
)

parser.add_argument(
    'image_path',
    help='Valid local path or URL of an image file',
)

parser.add_argument(
    'output_format',
    help='Desired output format: jpg, jpeg, png, webp',
)

parser.add_argument(
    'save_to',
    help='Local path for saving image, defaults to the current directory',
    nargs='?',
    default='.',
)


if __name__ == '__main__':
    args = parser.parse_args()
    convert_image(args.image_path, args.output_format, args.save_to)
