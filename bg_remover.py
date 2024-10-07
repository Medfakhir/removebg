import os
from flask import Flask, request, send_file
from flask_cors import CORS
import io
from rembg import remove

app = Flask(__name__)
CORS(app)

def remove_background(input_image):
    result = remove(input_image)
    return result

@app.route('/remove_background', methods=['POST'])
def handle_remove_background():
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400

    image_file = request.files['image']
    input_image = image_file.read()

    result = remove_background(input_image)

    return send_file(io.BytesIO(result), mimetype='image/png')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
