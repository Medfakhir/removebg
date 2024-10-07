import logging
from flask import Flask, request, send_file
from flask_cors import CORS
import io
from rembg import remove
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Enable CORS to allow Next.js frontend to communicate with Flask API

def remove_background(input_image):
    """Removes the background from an image."""
    try:
        logging.debug("Removing background from image")
        result = remove(input_image)
        return result
    except Exception as e:
        logging.error(f"Error removing background: {e}")
        raise  # Re-raise the exception for further handling

@app.route('/remove_background', methods=['POST'])
def handle_remove_background():
    """Handles the image upload and returns the image without background."""
    logging.debug("Received request to remove background")
    
    if 'image' not in request.files:
        logging.error("No image uploaded")
        return {'error': 'No image uploaded'}, 400

    image_file = request.files['image']
    input_image = image_file.read()

    logging.debug(f"Received image of size: {len(input_image)} bytes")

    # Remove the background from the image
    try:
        result = remove_background(input_image)
    except Exception as e:
        logging.error("Failed to process image")
        return {'error': str(e)}, 500  # Return a server error response

    # Return the processed image
    return send_file(io.BytesIO(result), mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
