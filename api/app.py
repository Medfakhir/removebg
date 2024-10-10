from flask import Flask, request, send_file
from flask_cors import CORS
import io
from rembg import remove

app = Flask(__name__)
CORS(app)  # Enable CORS to allow Next.js frontend to communicate with Flask API

def remove_background(input_image):
    """Removes the background from an image."""
    result = remove(input_image)
    return result

@app.route('/remove_background', methods=['POST'])
def handle_remove_background():
    """Handles the image upload and returns the image without background."""
    if 'image' not in request.files:
        return {'error': 'No image uploaded'}, 400

    image_file = request.files['image']
    input_image = image_file.read()

    # Remove the background from the image
    result = remove_background(input_image)

    # Return the processed image
    return send_file(io.BytesIO(result), mimetype='image/png')

# Comment out the app.run part for Vercel
# if __name__ == "__main__":
#     app.run(debug=True)
