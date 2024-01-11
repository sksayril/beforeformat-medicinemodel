# # # import cv2
# # # import base64
# # # import requests
# # # import time

# # # def capture_and_send():
# # #     cap = cv2.VideoCapture(0)

# # #     while True:
# # #         ret, frame = cap.read()
# # #         if not ret:
# # #             break

# # #         _, buffer = cv2.imencode('.jpg', frame)
# # #         frame_base64 = base64.b64encode(buffer).decode('utf-8')

# # #         try:
# # #             response = requests.post('http://192.168.29.214:5000/detect_objects', json={"image": frame_base64})
# # #             detected_objects = response.json().get('detected_objects')
# # #             print("Detected objects:", detected_objects)
# # #         except Exception as e:
# # #             print("Error sending frame:", str(e))

# # #         time.sleep(0.1)  # Add a small delay between requests

# # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # #             break

# # #     cap.release()
# # #     cv2.destroyAllWindows()

# # # if __name__ == '__main__':
# # #     capture_and_send()

# # import requests
# # import cv2

# # # Function to capture video from the camera
# # def capture_video():
# #     cap = cv2.VideoCapture(0)  # Access the default camera

# #     while True:
# #         ret, frame = cap.read()  # Read frames from the camera

# #         # Convert the frame to bytes
# #         _, img_encoded = cv2.imencode('.jpg', frame)
# #         img_bytes = img_encoded.tobytes()

# #         # Send the frame to the Flask server for object detection
# #         response = requests.post('http://192.168.29.214:5000/detect', files={'image': img_bytes})

# #         # Handle the detection results
# #         if response.status_code == 200:
# #             detections = response.json()['detections']
# #             # Process and display the detections as needed
# #             # For example, print them here
# #             print(detections)

# #         if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit if 'q' is pressed
# #             break

# #     cap.release()
# #     cv2.destroyAllWindows()

# # if __name__ == '__main__':
# #     capture_video()

# # import requests
# # import matplotlib.pyplot as plt
# # import matplotlib.patches as patches
# # from PIL import Image
# # import io

# # # Path to the image you want to send for detection
# # image_path = 'image.jpg'

# # # URL of your Flask API endpoint
# # api_url = 'http://192.168.29.214:5000/detect'  # Replace with your Flask API URL

# # # Read the image file
# # with open(image_path, 'rb') as file:
# #     image = file.read()

# # # Set up the payload for the POST request
# # files = {'image': (image_path, image, 'multipart/form-data')}

# # # Send the POST request to the Flask server
# # response = requests.post(api_url, files=files)

# # # Process the response
# # if response.status_code == 200:
# #     detections = response.json()
# #     print("Object Detections:")
# #     print(detections)

# #     # Display the image with bounding boxes
# #     img = Image.open(image_path)
# #     plt.figure(figsize=(8, 6))
# #     plt.imshow(img)

# #     ax = plt.gca()

# #     for detection in detections:
# #         # Extract box coordinates
# #         xmin = detection['xmin']
# #         ymin = detection['ymin']
# #         width = detection['xmax'] - xmin
# #         height = detection['ymax'] - ymin

# #         # Create a Rectangle patch
# #         rect = patches.Rectangle((xmin, ymin), width, height, linewidth=1, edgecolor='r', facecolor='none')

# #         # Add the patch to the Axes
# #         ax.add_patch(rect)

# #     plt.axis('off')  # Hide axis
# #     plt.show()

# # else:
# #     print("Failed to receive a valid response from the server.")

# # import cv2
# # import requests
# # import numpy as np

# # # URL of your Flask API endpoint
# # api_url = 'http://192.168.29.214:5000/detect'  # Replace with your Flask API URL

# # # Initialize the webcam
# # cap = cv2.VideoCapture(0)  # Use 0 for the default webcam, change the index if multiple webcams are connected

# # while True:
# #     # Capture frame-by-frame
# #     ret, frame = cap.read()

# #     # Convert the frame to bytes
# #     _, img_encoded = cv2.imencode('.jpg', frame)
# #     img_bytes = img_encoded.tobytes()

# #     # Set up the payload for the POST request
# #     files = {'image': ('webcam_image.jpg', img_bytes, 'multipart/form-data')}

# #     # Send the POST request to the Flask server
# #     response = requests.post(api_url, files=files)

# #     # Process the response
# #     if response.status_code == 200:
# #         detections = response.json()
# #         print("Object Detections:")
# #         print(detections)

# #         for detection in detections:
# #             # Extract box coordinates
# #             xmin = int(detection['xmin'] * frame.shape[1])
# #             ymin = int(detection['ymin'] * frame.shape[0])
# #             xmax = int(detection['xmax'] * frame.shape[1])
# #             ymax = int(detection['ymax'] * frame.shape[0])

# #             # Draw bounding box on the frame
# #             cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

# #         # Display the frame with bounding boxes
# #         cv2.imshow('Webcam with Object Detection', frame)

# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # # Release the webcam and close any open windows
# # cap.release()
# # cv2.destroyAllWindows()

# import cv2
# import requests

# # URL of your Flask API endpoint
# # api_url = 'http://192.168.29.214:5000/detect' 
# api_url = 'http://192.168.1.3:5000/detect' 


# cap = cv2.VideoCapture(0)  

# while True:
    
#     ret, frame = cap.read()

    
#     _, img_encoded = cv2.imencode('.jpg', frame)
#     img_bytes = img_encoded.tobytes()

    
#     files = {'image': ('webcam_image.jpg', img_bytes, 'multipart/form-data')}

    
#     response = requests.post(api_url, files=files)

    
#     if response.status_code == 200:
#         detections = response.json()
#         print("Object Detections:")
#         print(detections)

#         for detection in detections:
#             # Extract box coordinates
#             xmin = int(detection['xmin'])
#             ymin = int(detection['ymin'])
#             xmax = int(detection['xmax'])
#             ymax = int(detection['ymax'])

#             # Draw bounding box on the frame
#             cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)  # Green color

#             # Display class and confidence
#             cv2.putText(frame, f"{detection['name']} {detection['confidence']:.2f}",
#                         (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#         # Display the frame with bounding boxes
#         cv2.imshow('Webcam with Object Detection', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close any open windows
# cap.release()
# cv2.destroyAllWindows()
# import cv2
# import requests
# import numpy as np
# import random
# import string


# api_url = 'http://192.168.1.3:5000/detect'

# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()

#     _, img_encoded = cv2.imencode('.jpg', frame)
#     img_bytes = img_encoded.tobytes()

#     files = {'image': ('webcam_image.jpg', img_bytes, 'multipart/form-data')}
#     response = requests.post(api_url, files=files)

#     if response.status_code == 200:
#         detections = response.json()
#         print("Object Detections:")
#         print(detections)

#         for detection in detections:

#             xmin = int(detection['xmin'])
#             ymin = int(detection['ymin'])
#             xmax = int(detection['xmax'])
#             ymax = int(detection['ymax'])


#             cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2) 

#             cv2.putText(frame, f"{detection['name']} {detection['confidence']:.2f}",
#                         (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#             roi = frame[ymin:ymax, xmin:xmax]
#             if roi.size != 0: 
#                 filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '.jpg'
#                 cv2.imwrite(filename, roi)


#                 roi_encoded = cv2.imencode('.jpg', roi)[1]
#                 roi_bytes = roi_encoded.tobytes()
#                 files = {'image': (filename, roi_bytes, 'multipart/form-data')}

#                 upload_url = 'http://192.168.1.3:5000/upload'
#                 upload_response = requests.post(upload_url, files=files)
#                 if upload_response.status_code == 200:
#                     print(f"Uploaded {filename} to server")

#         cv2.imshow('Webcam with Object Detection', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import requests
# import numpy as np
import random
import string

api_url = 'http://192.168.29.214:5000/detect'
upload_url = 'http://192.168.29.214:5000/upload'  # URL to upload image

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()

    files = {'image': ('webcam_image.jpg', img_bytes, 'multipart/form-data')}
    response = requests.post(api_url, files=files)

    if response.status_code == 200:
        detections = response.json()
        print("Object Detections:")
        print(detections)

        for detection in detections:
            xmin = int(detection['xmin'])
            ymin = int(detection['ymin'])
            xmax = int(detection['xmax'])
            ymax = int(detection['ymax'])

            # Convert coordinates to integers and draw the bounding box
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            cv2.putText(frame, f"{detection['name']} {detection['confidence']:.2f}",
                        (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            roi = frame[ymin:ymax, xmin:xmax]
            if roi.size != 0: 
                filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '.jpg'
                cv2.imwrite(filename, roi)

                roi_encoded = cv2.imencode('.jpg', roi)[1]
                roi_bytes = roi_encoded.tobytes()

                # Send ROI to the server for saving
                files = {'image': (filename, roi_bytes, 'multipart/form-data')}
                upload_response = requests.post(upload_url, files=files)

                if upload_response.status_code == 200:
                    print(f"Uploaded {filename} to server")

        cv2.imshow('Webcam with Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
