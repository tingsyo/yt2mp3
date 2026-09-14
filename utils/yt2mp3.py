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
import yt-dlp
import eyed3
from pydub import AudioSegment

def extract_youtube_audio(video_url, output_filename='extracted_audio'):
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
    #
    print("Downloading and extracting audio...")
    with yt-dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print(f"Successfully saved as {output_filename}.mp3")
    #
    return(0)

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



