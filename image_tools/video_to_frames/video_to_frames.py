import os

import cv2

VIDEO_FILE_PATH = ''
FRAMES_FOLDER = 'frames'
os.makedirs(FRAMES_FOLDER, exist_ok=True)


def get_frames():
    video = cv2.VideoCapture(VIDEO_FILE_PATH)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    success, image = video.read()
    count = 0
    print(f'Saving {frame_count} frames to "{FRAMES_FOLDER}/"')

    while success:
        cv2.imwrite(os.path.join(FRAMES_FOLDER, f'{count:05}.jpg'), image)
        success, image = video.read()
        print(count)
        count += 1
