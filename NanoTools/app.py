from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
import qrcode
# from PIL import Image
from io import BytesIO
import os
from ascii_magic import AsciiArt, Back
import base64
import subprocess
from pytubefix import YouTube
import re
import ffmpeg

app = Flask(__name__,template_folder='templates')

# Use /tmp for Vercel since other directories are read-only
image_folder = '/tmp/images'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_qr', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        text = request.form.get('text')
        fill_color = request.form.get('fill_color', '#000000')
        back_color = request.form.get('back_color', '#ffffff')
        box_size = int(request.form.get('box_size', 10))

        # Generate QR code with customization options
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        # Save the QR code image to an in-memory file
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        # Convert the image to base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        # Pass the base64-encoded image to the template
        return render_template('generate_qr.html', qr_code=img_base64)

    return render_template('generate_qr.html')

video_folder = '/tmp/videos'
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

@app.route('/download', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        video_url = request.form.get('url')
        if not video_url:
            return jsonify({"error": "Please provide a YouTube URL."}), 400
        try:
            yt = YouTube(video_url)
            streams = yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by('resolution').desc()
            available_resolutions = []
            for i, stream in enumerate(streams, start=1):
                size = f"{stream.filesize // (1024 * 1024)} MB" if stream.filesize else "unknown"
                resolution_info = {
                    "index": i,
                    "resolution": stream.resolution,
                    "fps": stream.fps,
                    "size": size
                }
                available_resolutions.append(resolution_info)
            return render_template('select_resolution.html', video_url=video_url, available_resolutions=available_resolutions)

        except Exception as e:
            return jsonify({"error": f"Error fetching video info: {str(e)}"}), 500
    return render_template('download_video.html')

@app.route('/download/start', methods=['POST'])
def start_download():
    video_url = request.form.get('url')
    resolution = request.form.get('resolution')
    if not resolution:
        return jsonify({"error": "No resolution selected."}), 400
    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(res=resolution, file_extension="mp4").first()
        if not stream:
            return jsonify({"error": f"Resolution {resolution} not available."}), 400
        output_file = sanitize_filename(f"{yt.title}-{resolution}.mp4")
        if download_video_file(stream, output_file, video_url) == "Completed":
            return redirect(url_for('download_file', filename=output_file))
        else:
            raise KeyError
    except Exception as e:
        return jsonify({"error": f"Error downloading video: {str(e)}"}), 500

def download_video_file(stream, output_file, video_url):
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

        if not audio_stream:
            print("No audio streams available for this video.")
            return

        print("\nDownloading video...")
        video_file = stream.download(output_path=video_folder, filename="video.mp4")
        print("Video downloaded!")

        print("\nDownloading audio...")
        audio_file = audio_stream.download(output_path=video_folder, filename="audio.mp4")
        print("Audio downloaded!")

        # Merge video and audio using ffmpeg-python
        output_path = os.path.join(video_folder, output_file)
        print("\nMerging video and audio...")
        video_input = ffmpeg.input(os.path.join(video_folder, "video.mp4"))
        audio_input = ffmpeg.input(os.path.join(video_folder, "audio.mp4"))
        ffmpeg.output(video_input, audio_input, output_path, vcodec='copy', acodec='aac').run(overwrite_output=True)

        print(f"Download and merge complete! File saved as '{output_file}'")
        os.remove(os.path.join(video_folder, "video.mp4"))
        os.remove(os.path.join(video_folder, "audio.mp4"))
        return "Completed"
    except Exception as e:
        print(f"Error downloading or merging video: {str(e)}")

@app.route('/downloads/<filename>')
def download_file(filename):
    try:
        return send_from_directory(video_folder, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/ascii_magic')
def ascii_art():
    if request.method == 'POST':
        text = request.form.get('text')
        my_art = AsciiArt.from_image(f'images/{text}')
        my_art.to_html_file('ascii_art.html', columns=200, width_ratio=2)
        return render_template('ascii_art.html')
    else:
        return render_template('ascii_art.html')

if __name__ == '__main__':
    app.run(debug=True)
