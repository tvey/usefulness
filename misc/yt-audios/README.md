# Audio downloader

Download audios from YouTube video.

One dependency required: [yt-dlp](https://github.com/yt-dlp/yt-dlp), Python version: >= 3.8

## Usage

Run `main.py`, passing a video URL as an argument:

```bash
python main.py <video URL>

# for example
python main.py https://youtube.com/watch?v=MY5SatbZMAo
```

A folder named after the video ID is created, where the available audio files are saved.
