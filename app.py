from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH ='tomato-model.h5'

# Load your trained model
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    # Make prediction
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = x / 255.0
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds = np.argmax(preds, axis=1)
    
    # Map prediction index to label
    labels = ["Bacterial_spot", "Early_blight", "Late_blight", "Leaf_Mold", "Septoria_leaf_spot", "Spider_mites Two-spotted_spider_mite", "Target_Spot", "Tomato_Yellow_Leaf_Curl_Virus", "Tomato_mosaic_virus", "Healthy"]
    result = labels[preds[0]]
    
    return result
    
@app.route('/')
def hello_world():
    return 'Hello World'

# Define the endpoint to receive images
@app.route('/predict', methods=['POST', 'GET'])
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

            # Make prediction
            result = model_predict(image_path, model)

            # Return the path to the saved image and the prediction result
            return render_template('predict.html', image_path=image_path, result=result)
        except Exception as e:
            return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
    elif request.method == 'GET':
        try:
            # Read the saved image
            image_path = 'received_image.jpg'

            # Render the HTML template with the image path and an empty result
            return render_template('predict.html', image_path=image_path, result=None)
        except Exception as e:
            return jsonify({'error': f'Failed to retrieve image: {str(e)}'}), 500
