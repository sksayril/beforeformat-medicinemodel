from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock        
import cv2
import numpy as np
import requests
import random
import string

class WebcamApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Create the texture for displaying the camera feed
        self.texture = Texture.create(size=(640, 480), colorfmt='bgr')
        self.image = Image(texture=self.texture)
        self.layout.add_widget(self.image)

        # OpenCV setup
        self.cap = cv2.VideoCapture(0)

        # Schedule the update function to be called every frame
        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return self.layout

    def update(self, dt):
        ret, frame = self.cap.read()

        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        api_url = 'http://192.168.29.214:5000/detect'
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
                    upload_url = 'http://192.168.29.214:5000/upload'  # URL to upload image
                    files = {'image': (filename, roi_bytes, 'multipart/form-data')}
                    upload_response = requests.post(upload_url, files=files)

                    if upload_response.status_code == 200:
                        print(f"Uploaded {filename} to server")

            # Update the Kivy image widget with the camera frame
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            self.texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.image.canvas.ask_update()

    def on_stop(self):
        # Release the camera when the app is closed
        self.cap.release()

if __name__ == '__main__':
    WebcamApp().run()
