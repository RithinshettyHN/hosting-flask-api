#posting.py
import os
import requests

# URL of the Flask server endpoint to send the image to
flask_server_url = 'http://localhost:5000'  # Update this with your Flask server URL

def send_image_to_server(image_path):
    try:
        # Open the image file
        with open(image_path, 'rb') as image_file:
            # Send a POST request with the image file to the Flask server
            response = requests.post(flask_server_url, files={'image': image_file})
            if response.status_code == 200:
                print("Image successfully sent to server!")
            else:
                print(f"Failed to send image. Server returned status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while sending image: {e}")

# Replace 'image_path' with the path to the image captured by the camera module
image_path = r'C:\Users\Rithin\Downloads\Plantdisease\validation\Tomato_Bacterial_spot\00a7c269-3476-4d25-b744-44d6353cd921___GCREC_Bact.Sp 5807.jpg'

# Call the function to send the image to the Flask server
send_image_to_server(image_path)
