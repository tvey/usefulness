from folder import Folder

my_folder = Folder('path/to/my/folder')

duration = my_folder.duration
duration_seconds = my_folder.get_duration()
print(f'Total duration of “{my_folder.path.rsplit("/")[-1]}”: {duration}')
print(f'In seconds: {duration_seconds:.0f}')


if my_folder.subfolders:
    subfolder_durations = [
        (d.rsplit('/')[-1], Folder(d).duration) for d in my_folder.subfolders
    ]
    subfolder_durations.sort(key=lambda i: i[0].split('.')[0])

    for d in subfolder_durations:
        print(d[0], d[1])
