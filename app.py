from flask import Flask, request, send_file, jsonify
from PIL import Image
import io

app = Flask(__name__)

# Define the endpoint to receive images
@app.route('/', methods=['POST', 'GET'])
def receive_image():
    if request.method == 'POST':
        try:
            # Check if the request contains an image file
            if 'image' not in request.files:
                return jsonify({'error': 'No image found in request'}), 400

            # Get the image file from the request
            image_file = request.files['image']

            # Convert the image file to a PIL Image object
            image = Image.open(io.BytesIO(image_file.read()))

            # Save the image temporarily
            image_path = 'received_image.jpg'
            image.save(image_path)

            # Return the path to the saved image
            return jsonify({'image_path': image_path}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
    elif request.method == 'GET':
        try:
            # Read the saved image
            image_path = 'received_image.jpg'
            with open(image_path, 'rb') as image_file:
                # Send the image file in the response
                return send_file(io.BytesIO(image_file.read()), mimetype='image/jpeg')
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve image: {str(e)}'}), 500

