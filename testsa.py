# from pytubefix import YouTube

# def download_youtube_video():
#     print("Welcome to YouTube Video Downloader!")
#     # Get video URL from user
#     video_url = input("Enter the YouTube video URL: ").strip()

#     try:
#         # Create YouTube object
#         yt = YouTube(video_url)
        
#         # Display video title
#         print(f"Title: {yt.title}")
#         # downloader = yt.streams.get_highest_resolution()
#         # downloader.download()
#         # Display available streams
#         print("\nAvailable Streams:")
#         for stream in yt.streams.filter(progressive=True, file_extension='mp4'):
#             print(f"Resolution: {stream.resolution}, File size: {stream.filesize // (1024 * 1024)} MB")
        
#         # Ask user to choose resolution
#         resolution = input("\nEnter the resolution you want to download (e.g., 720p): ").strip()
#         video_stream = yt.streams.filter(res=resolution, progressive=True, file_extension='mp4').first()

#         if not video_stream:
#             print("The chosen resolution is not available. Please try again.")
#             return
        
#         # Download video
#         print("\nDownloading...")
#         video_stream.download()
#         print(f"Download complete! Video saved as '{yt.title}.mp4' in the current directory.")
    
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     download_youtube_video()


import os
from pytubefix import YouTube
import subprocess

def download_youtube_video():
    print("Welcome to YouTube Video Downloader!")
    video_url = input("Enter the YouTube video URL: ").strip()

    try:
        # Create YouTube object
        yt = YouTube(video_url)
        print(f"\nTitle: {yt.title}")

        # Display available video streams
        print("\nAvailable Video Streams:")
        video_streams = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc()
        for i, stream in enumerate(video_streams, start=1):
            print(f"{i}: Resolution: {stream.resolution}, FPS: {stream.fps}, File size: ~{stream.filesize // (1024 * 1024) if stream.filesize else 'unknown'} MB")

        # Ask user to choose a video stream
        choice = int(input("\nEnter the number of the resolution you want to download: "))
        selected_video_stream = video_streams[choice - 1]

        # Get corresponding audio stream
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()

        print("\nDownloading video...")
        video_file = selected_video_stream.download(filename="video.mp4")
        print("Video downloaded!")

        print("\nDownloading audio...")
        audio_file = audio_stream.download(filename="audio.mp4")
        print("Audio downloaded!")

        # Merge video and audio using FFmpeg
        output_file = yt.title + ".mp4"
        print("\nMerging video and audio...")
        merge_command = f'ffmpeg -y -i "video.mp4" -i "audio.mp4" -c:v copy -c:a aac "{output_file}"'
        subprocess.run(merge_command, shell=True, check=True)
        print(f"Download and merge complete! File saved as '{output_file}'")

        # Clean up temporary files
        os.remove("video.mp4")
        os.remove("audio.mp4")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_youtube_video()






# from yt_dlp import YoutubeDL

# def download_youtube_video(video_url):
#     try:
#         # Options for yt_dlp
#         ydl_opts = {
#             'format': 'bestvideo+bestaudio/best',  # Download best quality video+audio
#             'outtmpl': '%(title)s.%(ext)s',       # Save as title of video
#         }

#         with YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(video_url, download=True)  # Extract and download
#             print(f"Download complete: {info['title']}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     print("Welcome to YouTube Video Downloader!")
#     video_url = input("Enter the YouTube video URL: ").strip()
#     download_youtube_video(video_url)




# import os
# import subprocess

# def download_video_with_youget(video_url):
#     try:
#         # Set output directory (current directory)
#         output_dir = os.getcwd()

#         # Command to download video
#         command = ['you-get', '-o', output_dir, video_url]

#         # Run the command
#         subprocess.run(command, check=True)

#         print("Download completed successfully!")

#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred while downloading: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     print("Welcome to YouTube Video Downloader with you-get!")
#     video_url = input("Enter the YouTube video URL: ").strip()
#     download_video_with_youget(video_url)
