from flask import Flask, render_template, request, send_from_directory
import qrcode
from PIL import Image
from io import BytesIO
import os
from ascii_magic import AsciiArt, Back

app = Flask(__name__)

# # Ensure the 'images' folder exists
# image_folder = os.path.join(os.getcwd(), 'images')
# os.makedirs(image_folder, exist_ok=True)

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
        image_path = os.path.join(image_folder, f'QR_Code.png')
        img.save(image_path)

        return render_template('generate_qr.html', qr_code=image_path, os=os)
    else:
        return render_template('generate_qr.html', qr_code=None, os=os)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(image_folder, filename)

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
