# https://www.youtube.com/watch?v=nmA8Dke0Kow

import os
from pytubefix import YouTube
import subprocess
import re

def sanitize_filename(filename):
    """
    Sanitize the filename to make it safe for saving on the filesystem.
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def download_youtube_video():
    print("Welcome to YouTube Video Downloader!")
    video_url = input("Enter the YouTube video URL: ").strip()

    try:
        # Create YouTube object
        yt = YouTube(video_url)
        print(f"\nTitle: {yt.title}")

        # Sanitize the title to create a valid filename
        safe_title = sanitize_filename(yt.title)

        # Display available video streams
        print("\nAvailable Video Streams:")
        video_streams = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc()
        if not video_streams:
            print("No video streams available for this video.")
            return

        for i, stream in enumerate(video_streams, start=1):
            size = f"{stream.filesize // (1024 * 1024)} MB" if stream.filesize else "unknown"
            print(f"{i}: Resolution: {stream.resolution}, FPS: {stream.fps}, File size: ~{size}")

        # Ask user to choose a video stream
        while True:
            try:
                choice = int(input("\nEnter the number of the resolution you want to download: "))
                if 1 <= choice <= len(video_streams):
                    selected_video_stream = video_streams[choice - 1]
                    break
                else:
                    print("Invalid choice. Please select a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Get corresponding audio stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        if not audio_stream:
            print("No audio streams available for this video.")
            return

        print("\nDownloading video...")
        video_file = selected_video_stream.download(filename="video.mp4")
        print("Video downloaded!")

        print("\nDownloading audio...")
        audio_file = audio_stream.download(filename="audio.mp4")
        print("Audio downloaded!")

        # Merge video and audio using FFmpeg
        output_file = f"{safe_title}.mp4"
        print("\nMerging video and audio...")
        merge_command = [
            "ffmpeg", "-y",
            "-i", "video.mp4",
            "-i", "audio.mp4",
            "-c:v", "copy",
            "-c:a", "aac",
            output_file
        ]
        subprocess.run(merge_command, check=True)
        print(f"Download and merge complete! File saved as '{output_file}'")

        # Clean up temporary files
        os.remove("video.mp4")
        os.remove("audio.mp4")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_youtube_video()
