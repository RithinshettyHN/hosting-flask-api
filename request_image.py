import requests
from PIL import Image
from io import BytesIO

# URL of the Flask server endpoint to request the image from
server_url = 'http://localhost:5000'

def request_image_from_server():
    try:
        # Send a GET request to the server to get the image path
        response = requests.get(server_url)
        if response.status_code == 200:
            # Check if the response content type is JSON
            if response.headers['content-type'] == 'application/json':
                # Parse the JSON response
                data = response.json()
                image_path = data.get('image_path', '')
                
                # Send a GET request to download the image
                image_response = requests.get(server_url + '/' + image_path)
                if image_response.status_code == 200:
                    # Display the image
                    img = Image.open(BytesIO(image_response.content))
                    img.show()
                else:
                    print(f"Failed to download image. Server returned status code: {image_response.status_code}")
            else:
                # Directly handle the image response as binary data
                img = Image.open(BytesIO(response.content))
                img.show()
        else:
            print(f"Failed to request image. Server returned status code: {response.status_code}")
    except Exception as e:
        print(f"Error occurred while requesting image: {e}")

# Call the function to request the image from the server
request_image_from_server()
