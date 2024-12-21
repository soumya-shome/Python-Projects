# https://www.youtube.com/watch?v=nmA8Dke0Kow

from pytubefix import YouTube

import os

proxy = "http://141.11.103.136:8080"
os.environ["http_proxy"] = proxy
os.environ["https_proxy"] = proxy

# Then proceed with YouTube video downloading


def download_youtube_video():
    print("Welcome to YouTube Video Downloader!")
    video_url = input("Enter the YouTube video URL: ").strip()

    try:
        yt = YouTube(video_url, proxies={"http": proxy, "https": proxy})
        # yt = YouTube(video_url, use_po_token=True)  # Updated line
        print(f"Title: {yt.title}")

        print("\nAvailable Streams:")
        for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
            print(f"Resolution: {stream.resolution}, File size: {stream.filesize // (1024 * 1024)} MB")

        resolution = input("\nEnter the resolution you want to download (e.g., 720p): ").strip()
        video_stream = yt.streams.filter(res=resolution, progressive=True, file_extension='mp4').first()

        if not video_stream:
            print("The chosen resolution is not available. Please try again.")
            return

        print("\nDownloading...")
        video_stream.download()
        print(f"Download complete! Video saved as '{yt.title}.mp4' in the current directory.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_youtube_video()
