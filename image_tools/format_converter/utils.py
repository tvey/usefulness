import os
from pathlib import Path
from urllib.parse import urlparse

import requests

FORMATS = ['jpg', 'png', 'webp']


def is_url(value: str) -> bool:
    return urlparse(value).scheme != ''


def verify_output_format(format_value: str) -> str:
    format_value = format_value.lower()

    if not format_value in FORMATS:
        raise ValueError(f'Unsupported format: {format_value}')
    return format_value


def verify_path(path_value: str) -> bool:
    if not os.path.exists(path_value):
        raise ValueError(f'Unable to access {path_value}')
    return True


def get_filename(value: str) -> str:
    if is_url(value):
        value = urlparse(value).path
    return Path(value).stem


def get_input_format(value: str) -> str:
    if is_url(value):
        value = urlparse(value).path
    return os.path.splitext(value)[-1][1:]  # strip the dot


def request_image(url: str) -> bytes:
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise ValueError(f'Unable to get image from: {url}')
    return r.raw
