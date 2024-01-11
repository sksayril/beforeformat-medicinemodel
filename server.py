# # from flask import Flask, request, jsonify
# # import base64
# # import torch
# # from PIL import Image
# # from io import BytesIO

# # app = Flask(__name__)

# # # Function to perform object detection using YOLOv5
# # def detect_objects(image_base64):
# #     try:
# #         # Decode base64 image data
# #         image = Image.open(BytesIO(base64.b64decode(image_base64)))

# #         # Assuming you've loaded your YOLOv5 model previously
# #         model = torch.hub.load('ultralytics/yolov5', 'custom', path='test.pt', force_reload=True)
# #         model.eval()

# #         # Placeholder code for object detection using the loaded model
# #         # Replace this with your actual object detection code
# #         results = model(image)  # Example inference
# #         detected_objects = results.pandas().xyxy[0].to_dict(orient='records')  # Example result

# #         return detected_objects
# #     except Exception as e:
# #         return str(e)

# # @app.route('/detect_objects', methods=['POST'])
# # def handle_detection():
# #     data = request.get_json()
# #     image_base64 = data['image']

# #     # Perform object detection
# #     detected_objects = detect_objects(image_base64)

# #     # Return the detected objects as a response
# #     return jsonify({"detected_objects": detected_objects})

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5000, debug=True)  # Run the Flask app

# # from flask import Flask, request, jsonify
# # import torch

# # app = Flask(__name__)

# # # Load the YOLOv5 model
# # model = torch.hub.load('ultralytics/yolov5', 'custom', path='test.pt', force_reload=True)
# # model.eval()

# # @app.route('/detect', methods=['POST'])
# # def detect_objects():
# #     if 'image' not in request.files:
# #         return jsonify({'error': 'No image sent'})

# #     image = request.files['image']
# #     img_bytes = image.read()

# #     results = model(img_bytes)  # Perform object detection on the received image bytes

# #     return jsonify({'detections': results.pandas().to_json(orient='records')})

# # if __name__ == '__main__':
# #     app.run(debug=True)

# import torch
# from flask import Flask, request, jsonify
# from PIL import Image
# import io

# app = Flask(__name__)

# # Load the YOLOv5 model from the local path
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='./test.pt', force_reload=False)
# model.eval()

# @app.route('/detect', methods=['POST'])
# def detect_objects():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image sent'})

#     image = request.files['image']
#     img_bytes = image.read()

#     # Preprocess image bytes
#     img = Image.open(io.BytesIO(img_bytes)).convert('RGB')  # Read bytes as an image
#     img = img.resize((640, 640))  # Resize image to match the model input size

#     # Convert image to tensor and normalize
#     img_tensor = torch.tensor(img, dtype=torch.float32) / 255.0  # Normalize to [0, 1]
#     img_tensor = img_tensor.permute(2, 0, 1)  # Reorder dimensions to (channels, height, width)

#     # Perform object detection on the preprocessed image tensor
#     results = model(img_tensor.unsqueeze(0))  # Unsqueeze to add batch dimension

#     # Extracting labels and bounding boxes to return
#     detections = results.pandas().xyxy[0].to_dict(orient='records')

#     return jsonify({'detections': detections})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000,debug=True)

# app.py

# import torch
# from flask import Flask, request, jsonify
# from PIL import Image
# import io
# import os
# app = Flask(__name__)

# # Load the YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='test.pt', force_reload=True)
# model.eval()

# @app.route('/detect', methods=['POST'])
# def object_detection():
#     # Receive image from client
#     image = request.files['image']
    
#     # Read the image file and preprocess
#     img = Image.open(io.BytesIO(image.read())).convert("RGB")
#     results = model(img) 
#     if not os.path.exists('data'):
#         os.makedirs('data')

#     # Retrieve the uploaded file
#     uploaded_file = request.files['image']

#     # Generate a random filename and save the uploaded file
#     filename = os.path.join('data', uploaded_file.filename)
#     uploaded_file.save(filename)

#     # return jsonify({'message': 'Image uploaded successfully'})

#     # Extract detection results
#     detections = results.pandas().xyxy[0].to_dict('records')  # Convert detections to a dictionary

#     # Return the detections
#     return jsonify(detections)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
# import torch
# from flask import Flask, request, jsonify
# from PIL import Image
# import io
# import os
# from werkzeug.utils import secure_filename


# app = Flask(__name__)

# # Load the YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='test.pt', force_reload=True)
# model.eval()

# @app.route('/detect', methods=['POST'])
# def object_detection():
#     # Receive image from client
#     image = request.files['image']
    
#     # Read the image file and preprocess
#     img = Image.open(io.BytesIO(image.read())).convert("RGB")
#     results = model(img) 

#     # Create the 'Newdata' folder if it doesn't exist
#     if not os.path.exists('ROIs'):
#         os.makedirs('ROIs')

#     filename = os.path.join('ROIs', secure_filename(image.filename))
#     image.save(filename)
#     # Extract detection results
#     detections = results.pandas().xyxy[0].to_dict('records')  # Convert detections to a dictionary

#     # Return the detections
#     return jsonify(detections)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

import torch
from flask import Flask, request, jsonify
from PIL import Image,UnidentifiedImageError
import io
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='test.pt', force_reload=True)
model.eval()

@app.route('/detect', methods=['POST'])
def object_detection():
    print("Imageeeeeshbaskjasasjnsanjalnjsasljnasljnaslnj")
    # Receive image from client
    try:
        image = request.files['image']
        print("This is Image",image)
        image_type = image.content_type
        
        # Print the received image type
        print(f"Received image type: {image_type}")

        # Read the image file and preprocess
        img = Image.open(io.BytesIO(image.read())).convert("RGB")
        results = model(img)
        print(results) 

        # Create the 'ROIs' folder if it doesn't exist
        if not os.path.exists('ROIs'):
            os.makedirs('ROIs')

        filename = os.path.join('ROIs', secure_filename(image.filename))
        image.save(filename)
        # Extract detection results
        detections = results.pandas().xyxy[0].to_dict('records')  # Convert detections to a dictionary

        # Return the detections
        return jsonify(detections)
    except UnidentifiedImageError as e:
        return 'Invalid image format. Please upload a valid image.', 400
@app.route('/upload', methods=['POST'])
def upload_image():
    uploaded_file = request.files['image']

    if uploaded_file.filename != '':
        # Save the uploaded image to the 'serverfile_folder'
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join('serverfile_folder', filename))

        return 'File uploaded successfully', 200

    return 'Invalid file', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
