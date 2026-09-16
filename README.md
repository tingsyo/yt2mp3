# yt2mp3

This is a small project that provides simple python tools to c1reate mp3 files from YouTube.

## Pre-requisites

### Software:
- [python](https://www.python.org/): the tools are developed and tested with Python-3.13.
- [ffmpeg](https://ffmpeg.org/): for processing video/audio files
- [deno](https://deno.com/): a javascript engine used by [yt-dlp](https://github.com/yt-dlp/yt-dlp).

### Python Packages
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): a feature-rich command-line audio/video downloader with support for thousands of sites. The project is a fork of youtube-dl based on the now inactive youtube-dlc.
- [eyed3](https://pypi.org/project/eyeD3/): a Python tool for working with audio files, specifically MP3 files containing ID3 metadata (i.e. song info).
- [pydub](https://pypi.org/project/pydub/): to manipulate audio with an simple and easy high level interface.
- [pandas](https://pypi.org/project/pandas/): A Powerful Python Data Analysis Toolkit.

## Usage

1. Make sure that you have installed all pre-requisites.
2. Download this repository.
3. Prepare a list of songs in `.csv` format. See `playlist/MySongs-1990.csv` for example.
4. In command line:
```bash
python utils/yt2mp3.py -i playlist/MySongs-1990.csv
```

You will have the downloaded `.mp3` files stored in `downloads/`.


