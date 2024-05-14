import os
import argparse

import yt_dlp


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download audios from Youtube video'
    )
    parser.add_argument('url', help='Video URL')
    return parser.parse_args()


def download_audios(video_url: str):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_id = info['id']
        formats = info.get('formats', [])

        if formats:
            audios = [
                i
                for i in info['formats']
                if i.get('acodec') == 'opus'
                and i.get('resolution') == 'audio only'
                and i.get('quality') == 3.0
            ]

    save_to = os.path.join(os.getcwd(), video_id)

    if not os.path.exists(save_to):
        os.makedirs(save_to)

    for audio in audios:
        ydl_opts = {
            'extract_audio': True,
            'format': f"{audio['format_id']}",
            'outtmpl': os.path.join(save_to, '%(title)s_%(format_note)s.mp3'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])


if __name__ == '__main__':
    args = parse_args()
    url = args.url
    download_audios(url)
