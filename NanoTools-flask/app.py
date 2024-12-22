from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import os
import re
import youtube_dl
from io import BytesIO
import base64
import ffmpeg
import subprocess

app = Flask(__name__, template_folder='templates')

# Use /tmp for Vercel since other directories are read-only
video_folder = '/tmp/videos'
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        video_url = request.form.get('url')
        if not video_url:
            return jsonify({"error": "Please provide a YouTube URL."}), 400

        try:
            # Fetch video info using youtube_dl
            ydl_opts = {
                'quiet': True,
                'format': 'bestvideo+bestaudio/best',
                'noplaylist': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                video_title = sanitize_filename(info.get('title', 'video'))
                available_formats = [
                    {
                        "format_id": f["format_id"],
                        "resolution": f.get("height", "audio-only"),
                        "filesize": f.get("filesize", None)
                    }
                    for f in info['formats'] if f.get('filesize')
                ]

            return render_template(
                'select_resolution.html',
                video_url=video_url,
                video_title=video_title,
                available_formats=available_formats
            )
        except Exception as e:
            return jsonify({"error": f"Error fetching video info: {str(e)}"}), 500

    return render_template('download_video.html')

@app.route('/download/start', methods=['POST'])
def start_download():
    video_url = request.form.get('url')
    format_id = request.form.get('format_id')

    if not format_id:
        return jsonify({"error": "No format selected."}), 400

    try:
        # Download video using youtube_dl
        video_path = os.path.join(video_folder, 'video.mp4')
        audio_path = os.path.join(video_folder, 'audio.mp4')
        output_path = os.path.join(video_folder, 'output.mp4')

        ydl_opts = {
            'format': format_id,
            'outtmpl': video_path,
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url)
            video_title = sanitize_filename(info['title'])

        # Merge video and audio using ffmpeg
        print("Merging video and audio...")
        video_input = ffmpeg.input(video_path)
        audio_input = ffmpeg.input(audio_path)
        ffmpeg.output(video_input, audio_input, output_path, vcodec='copy', acodec='aac').run(overwrite_output=True)

        print(f"Merge complete! File saved as {output_path}")
        return redirect(url_for('download_file', filename='output.mp4'))

    except Exception as e:
        return jsonify({"error": f"Error downloading or merging video: {str(e)}"}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    try:
        return send_from_directory(video_folder, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    # Launch Flask application
    subprocess.Popen(['python', 'google_signin.py'])  # Start Google sign-in script
    app.run(debug=True)
