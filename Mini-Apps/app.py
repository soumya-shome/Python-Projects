from flask import Flask, render_template, request, send_from_directory
import qrcode
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

# Ensure the 'images' folder exists
image_folder = os.path.join(os.getcwd(), 'images')
os.makedirs(image_folder, exist_ok=True)

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

        # Save the QR code image to the 'images' folder
        image_path = os.path.join(image_folder, f'{text}_{box_size}_{fill_color}_{back_color}.png')
        img.save(image_path)

        return render_template('generate_qr.html', qr_code=image_path, os=os)
    else:
        return render_template('generate_qr.html', qr_code=None, os=os)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(image_folder, filename)

@app.route('/ascii_magic')
def ascii_art():
    return render_template('ascii_art.html')

if __name__ == '__main__':
    app.run(debug=True)
