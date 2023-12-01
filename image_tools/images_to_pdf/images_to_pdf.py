import os

from PIL import Image


def convert_to_pdf(
    images_folder: str,
    filename: str = '',
    output_folder: str = '',
):
    if not filename:
        filename = f'{os.path.basename(images_folder)}.pdf'
    else:
        filename = f'{filename}.pdf'
    if not output_folder:
        output_folder = os.path.dirname(images_folder)

    output_file = os.path.join(output_folder, filename)

    images = [
        os.path.join(images_folder, i)
        for i in os.listdir(images_folder)
        if os.path.splitext(i)[1] in ['.jpg', '.jpeg', '.png']
    ]
    if images:
        converted_images = []

        for image in images:
            try:
                converted_images.append(Image.open(image).convert('RGB'))
            except PIL.UnidentifiedImageError:
                print(f'! Not added: {image}')

        converted_images = [Image.open(i).convert('RGB') for i in images]
        converted_images[0].save(
            output_file,
            'PDF',
            resolution=100.0,
            save_all=True,
            append_images=converted_images[1:],
        )
        print(f'File created: {output_file}')


def batch_convert(root):
    subfolders = [os.path.join(root, i) for i in os.listdir(root)]
    for folder in subfolders:
        print(f'Working on: {folder}')
        convert_to_pdf(folder)
