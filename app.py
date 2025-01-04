from flask import Flask, render_template, request, send_file, jsonify
from flask_cors import CORS
import qrcode
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('qr.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    try:
        # Extract data from JSON request
        data = request.json.get('data')
        fg_color = request.json.get('fg_color', '#000000')  # Default: Black
        bg_color = request.json.get('bg_color', '#FFFFFF')  # Default: White

        if not data:
            return jsonify({'error': 'Data is required'}), 400

        # Concatenate multiline data
        data_str = "\n".join(data)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_str)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill=fg_color, back_color=bg_color)

        # Save QR code to BytesIO object
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
