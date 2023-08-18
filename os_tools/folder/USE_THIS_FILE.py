import os
import re

from folder import Folder


def parse_filesize(size: str) -> int:
    units = {
        'B': 1,
        'BYTES': 1,
        'KB': 2**10,
        'MB': 2**20,
        'GB': 2**30,
        'TB': 2**40,
    }
    size = size.strip().upper()

    if not 'B' in size or not any(i.isdigit() for i in size):
        raise ValueError('Make sure both unit and size are specified')

    if not ' ' in size:
        size = re.sub(r'([KMGT]?B)', r' \1', size)

    number, unit = size.split()
    return int(float(number) * units[unit])


# folders = [
#     '/home/tanya/Courses/!!!Lynda - Programming Foundations - Complete Collection/'
# ]

# for ff in folders:
#     my_folder = Folder(ff)
#     duration = my_folder.duration
#     print(f'{duration} ----- {my_folder.path.rsplit("/")[-1]}')



# if my_folder.subfolders:
#     subfolder_durations = [
#         (d.rsplit('/')[-1], Folder(d).duration) for d in my_folder.subfolders
#     ]
#     subfolder_durations.sort(key=lambda i: i[0].split('.')[0])

#     for d in subfolder_durations:
#         print(d[0], d[1])



root = r'E:\Audiobooks'


subfolders = [os.path.join(root, i) for i in os.listdir(root)]

sizes = []
for folder in subfolders:
    if os.path.isdir(folder):
        f = Folder(folder)
        try:
            sizes.append((f.size, f))
        except:
            print('???', folder)

sizes.sort(key=lambda i: parse_filesize(i[0]), reverse=True)

for i in sizes:
    print(f'{i[0]} -- {i[1]}')
