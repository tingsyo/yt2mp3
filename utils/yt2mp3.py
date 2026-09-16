#!/usr/bin/env python3
"""
yt2mp3.py - Tool: 
1. Download YouTube video/audio using yt-dlp.
2. Normalize the volume of the audio.
3. Add meta data to the audio and export it to mp3 format.
"""
import argparse
import os
import sys
from pathlib import Path
import yt_dlp
import eyed3
from pydub import AudioSegment
import types
import pandas as pd

# Create a fake audioop module to bypass the pydub import crash
if sys.version_info >= (3, 13):
    sys.modules['audioop'] = types.ModuleType('audioop')
    sys.modules['pyaudioop'] = types.ModuleType('pyaudioop')

def extract_youtube_audio(yt_url, output_filename=None):
     # Use the video title as output_filename if not specified
    if output_filename is None:
        with yt_dlp.YoutubeDL({'skip_download': True,}) as ydl:
            info = ydl.extract_info(yt_url, download=False)
            output_filename = info['title'].replace(' ','_')
            print(f"output_filename is not specified, set title: {info['title']}")
   # Set download options
    ydl_opts = {
        # Select the best quality audio-only stream
        'format': 'bestaudio/best',
        # Post-processor configurations to convert the stream
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',      # Options: 'mp3', 'wav', 'aac', 'flac', etc.
            'preferredquality': '192',    # Audio bitrate quality
        }],
        # Output template for the file name
        'outtmpl': f'{output_filename}.%(ext)s',
    }
    # Download
    print("Downloading and extracting audio...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
    print(f"Successfully saved as {output_filename}.mp3")
    #
    return(output_filename)

def normalize_average_loudness(audio_uri, target_dBFS=-20.0):
    # 1. Load your audio file
    audio = AudioSegment.from_file(audio_uri)
    # 2. Normalize to a designated target (e.g., -20.0 dBFS)
    # Calculate how much gain is needed to hit the target
    change_in_dBFS = target_dBFS - audio.dBFS
    normalized_audio = audio.apply_gain(change_in_dBFS)
    # 3. Export the processed audio
    normalized_audio.export(audio_uri, format="mp3")
    return(0)


def edit_mp3_metadata(audio_uri, metadata):
    ''' Modify the metadata of specified mp3 file. '''
    # 1. Load the audio file
    audiofile = eyed3.load(audio_uri)
    # 2. Modify the tags
    audiofile.tag.title = metadata["title"]
    audiofile.tag.artist = metadata["artist"]
    audiofile.tag.album = metadata["album"]
    audiofile.tag.date = metadata["date"]
    # 3. Save the changes
    audiofile.tag.save()
    return(0)

def youtube_to_mp3(yt_url, metadata=None, output_filename=None):
    ''' Extract the audio from the yt-url, add metadata, and export to a mp3 file. '''
    ofilename = extract_youtube_audio(yt_url=yt_url, output_filename=output_filename)
    normalized = normalize_average_loudness(audio_uri=ofilename+".mp3")
    # Process metada
    if metadata is None:
        metadata = {"title": ofilename, "artist":"unknown", "album":"unknown","date":"unknown"}
    else:
        if not metadata["title"]:
            metadata["title"] = ofilename
        if not metadata["artist"]:
            metadata["artist"] = "unknown"
        if not metadata["album"]:
            metadata["album"] = "unknown"
        if not metadata["date"]:
            metadata["date"] = "unknown"
    edited = edit_mp3_metadata(ofilename+".mp3", metadata)
    return(edited)


def main():
    parser = argparse.ArgumentParser(description="Download YouTube video or audio locally.")
    #parser.add_argument("--url", "-u", required=True, help="YouTube video URL")
    parser.add_argument("--input", "-i", required=True, help="List of music in csv format.")
    parser.add_argument("--output-dir", "-o", default="downloads", help="Output directory (default: 'downloads')")
    parser.add_argument("--audio-only", "-a", action="store_true", help="Download audio track only (WAV format)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress verbose output")
    args = parser.parse_args()
    # Read list
    musiclist = pd.read_csv(args.input, dtype=str, na_values="unknown")
    print("The playlist contains "+ str(musiclist.shape[0]) +" songs.")
    # Loop through list
    for row in musiclist.itertuples():
        # Parse data
        yt_url = row.youtube
        metadata = {
            'title': str(row.name),
            'artist': str(row.artist),
            'album': str(row.album),
            'date': str(row.date),
        }
        output_filename = "downloads/"+row.date+"_"+row.name
        print(metadata)
        # download and processing
        try:
            youtube_to_mp3(yt_url, metadata, output_filename)
        except Exception as e:
            print(f"[-] Error downloading video: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
