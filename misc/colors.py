import random


def generate_hex_color():
    return '#' + str(hex(random.randint(0, 16777215)))[2:]