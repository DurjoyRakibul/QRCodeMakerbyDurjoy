from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS  # Import CORS
import qrcode
from io import BytesIO
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to generate the QR code
@app.route('/generate', methods=['POST'])
def generate_qr():
    data = request.json.get('data')  # Extract data from the JSON payload
    fg_color = request.json.get('fg_color', '#000000')  # Default black color for foreground
    bg_color = request.json.get('bg_color', '#FFFFFF')  # Default white color for background

    if not data:
        return jsonify({'error': 'Data is required'}), 400

    # Concatenate the multiple lines of data with a newline separator
    data_str = "\n".join(data)  # This will join the data items with a newline between them

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_str)
    qr.make(fit=True)

    # Create the image for the QR code with the specified colors
    img = qr.make_image(fill=fg_color, back_color=bg_color)

    # Save the QR code to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    # Return the QR code as a downloadable file
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

if __name__ == '__main__':
    # Get the port from the environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
