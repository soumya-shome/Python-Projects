from flask import Flask, render_template, request, send_from_directory
import qrcode
from PIL import Image
from io import BytesIO
import os
from ascii_magic import AsciiArt, Back
import base64
from pytubefix import YouTube

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


@app.route('/download_video', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        video_url = request.form.get('video_url')

        try:
            # Create YouTube object
            yt = YouTube(video_url)
            
            # Get the highest resolution progressive stream (video + audio)
            video_stream = yt.streams.get_highest_resolution()

            # Download the video to an in-memory file
            video_buffer = BytesIO()
            video_stream.stream_to_buffer(video_buffer)
            video_buffer.seek(0)

            # Return the video file as a downloadable response
            return send_file(
                video_buffer,
                as_attachment=True,
                download_name=f"{yt.title}.mp4",
                mimetype="video/mp4"
            )

        except Exception as e:
            return f"An error occurred: {e}", 500

    return render_template('download_video.html')



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
