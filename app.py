import logging
from flask import Flask, request, send_file
from flask_cors import CORS
import io
from rembg import remove
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

def remove_background(input_image):
    """Removes the background from an image."""
    logging.debug("Removing background from image")
    result = remove(input_image)
    return result

@app.route('/remove_background', methods=['POST'])
def handle_remove_background():
    """Handles the image upload and returns the image without background."""
    logging.debug("Received request to remove background")
    if 'image' not in request.files:
        logging.error("No image uploaded")
        return {'error': 'No image uploaded'}, 400

    image_file = request.files['image']
    input_image = image_file.read()

    # Remove the background from the image
    result = remove_background(input_image)

    # Return the processed image
    return send_file(io.BytesIO(result), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
